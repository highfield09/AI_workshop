"""Single-host JupyterHub sandbox with DockerSpawner and per-user LiteLLM keys.

This configuration is intentionally designed for a small trusted workshop pilot.
It uses generated per-user passwords. Replace this local dictionary authenticator
with institutional OAuth/OIDC before a real public deployment.
"""

from __future__ import annotations

import fcntl
import json
import os
from secrets import compare_digest
from pathlib import Path
from typing import Any

import requests
from jupyterhub.auth import Authenticator
from traitlets import Dict

c = get_config()  # noqa: F821 - provided by JupyterHub


def csv_set(name: str, default: str) -> set[str]:
    raw = os.getenv(name, default)
    return {item.strip() for item in raw.split(",") if item.strip()}


# ---------------------------------------------------------------------------
# Hub networking and persistence
# ---------------------------------------------------------------------------
c.JupyterHub.bind_url = "http://0.0.0.0:8000"
c.JupyterHub.hub_bind_url = "http://0.0.0.0:8081"
c.JupyterHub.hub_connect_url = "http://jupyterhub:8081"
c.JupyterHub.db_url = "sqlite:////srv/jupyterhub/jupyterhub.sqlite"
c.JupyterHub.cookie_secret = bytes.fromhex(os.environ["JUPYTERHUB_COOKIE_SECRET"])
c.JupyterHub.log_level = "INFO"

# ---------------------------------------------------------------------------
# Workshop-only authentication with a unique generated password per username.
# Passwords are stored in the root-controlled Hub environment for this sandbox.
# ---------------------------------------------------------------------------
class DictionaryAuthenticator(Authenticator):
    passwords = Dict(config=True)

    async def authenticate(self, handler, data):
        username = self.normalize_username(data.get("username", ""))
        supplied = data.get("password", "")
        expected = self.passwords.get(username, "")
        # Always compare, including for unknown users, to reduce timing leakage.
        if compare_digest(str(supplied), str(expected)) and expected:
            return username
        return None


c.JupyterHub.authenticator_class = DictionaryAuthenticator
c.DictionaryAuthenticator.passwords = json.loads(
    os.environ["JUPYTERHUB_USER_PASSWORDS_JSON"]
)
c.Authenticator.allowed_users = csv_set(
    "JUPYTERHUB_ALLOWED_USERS", "instructor,student1,student2"
)
c.Authenticator.admin_users = csv_set("JUPYTERHUB_ADMIN_USERS", "instructor")
c.Authenticator.allow_all = False

# ---------------------------------------------------------------------------
# Per-user containers
# ---------------------------------------------------------------------------
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
c.DockerSpawner.image = os.getenv(
    "JUPYTER_USER_IMAGE", "vibe-classroom-user:latest"
)
c.DockerSpawner.network_name = os.getenv("DOCKER_NETWORK_NAME", "vibe-jhub-net")
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.remove = True
c.DockerSpawner.name_template = "vibe-{username}"
c.DockerSpawner.cmd = ["start-singleuser.py"]
c.Spawner.default_url = "/lab"
c.DockerSpawner.notebook_dir = "/home/jovyan/work"
c.DockerSpawner.volumes = {
    "vibe-user-{username}": "/home/jovyan/work",
}
c.DockerSpawner.read_only_volumes = {
    "vibe-course-materials": "/home/jovyan/course_materials",
}
c.DockerSpawner.mem_limit = os.getenv("STUDENT_MEM_LIMIT", "4G")
c.DockerSpawner.cpu_limit = float(os.getenv("STUDENT_CPU_LIMIT", "2.0"))
c.DockerSpawner.extra_host_config = {
    "pids_limit": 512,
    "cap_drop": ["ALL"],
    "security_opt": ["no-new-privileges:true"],
}
student_llm_base_url = os.getenv(
    "STUDENT_LLM_BASE_URL", "http://api-proxy:8080/v1"
)
c.DockerSpawner.environment = {
    "JUPYTER_ENABLE_LAB": "yes",
    # OPENAI_BASE_URL is used by the current OpenAI Python client.
    # OPENAI_API_BASE is also supplied for compatible notebook extensions.
    "OPENAI_BASE_URL": student_llm_base_url,
    "OPENAI_API_BASE": student_llm_base_url,
    "CLASSROOM_MODEL": os.getenv("STUDENT_LLM_MODEL", "classroom-qwen"),
    "PYTHONUNBUFFERED": "1",
}

# ---------------------------------------------------------------------------
# Automatic per-user LiteLLM virtual keys
# ---------------------------------------------------------------------------
KEY_STORE = Path("/srv/jupyterhub/student_keys.json")
KEY_LOCK = Path("/srv/jupyterhub/student_keys.lock")
LITELLM_ADMIN_URL = os.environ["LITELLM_ADMIN_URL"].rstrip("/")
LITELLM_MASTER_KEY = os.environ["LITELLM_MASTER_KEY"]


def _read_key_store() -> dict[str, dict[str, Any]]:
    if not KEY_STORE.exists():
        return {}
    try:
        return json.loads(KEY_STORE.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def _write_key_store(data: dict[str, dict[str, Any]]) -> None:
    temp = KEY_STORE.with_suffix(".tmp")
    temp.write_text(json.dumps(data, indent=2, sort_keys=True))
    os.chmod(temp, 0o600)
    temp.replace(KEY_STORE)


def _generate_student_key(username: str) -> dict[str, Any]:
    payload = {
        "models": [os.getenv("STUDENT_LLM_MODEL", "classroom-qwen")],
        "user_id": username,
        "key_alias": f"jupyterhub-{username}",
        "duration": os.getenv("STUDENT_KEY_DURATION", "30d"),
        "rpm_limit": int(os.getenv("STUDENT_RPM_LIMIT", "6")),
        "tpm_limit": int(os.getenv("STUDENT_TPM_LIMIT", "12000")),
        "max_parallel_requests": int(
            os.getenv("STUDENT_MAX_PARALLEL_REQUESTS", "1")
        ),
        "metadata": {
            "source": "jupyterhub",
            "jupyterhub_username": username,
        },
    }
    response = requests.post(
        f"{LITELLM_ADMIN_URL}/key/generate",
        headers={
            "Authorization": f"Bearer {LITELLM_MASTER_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()
    key = result.get("key")
    if not key:
        raise RuntimeError(f"LiteLLM did not return a key: {result}")
    return {
        "key": key,
        "expires": result.get("expires"),
        "key_alias": payload["key_alias"],
        "models": payload["models"],
    }


def provision_llm_key(spawner) -> None:
    """Create a virtual key once and inject it into only that user's container."""
    username = spawner.user.name
    KEY_LOCK.touch(mode=0o600, exist_ok=True)
    with KEY_LOCK.open("r+") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        store = _read_key_store()
        record = store.get(username)
        if not record or not record.get("key"):
            record = _generate_student_key(username)
            store[username] = record
            _write_key_store(store)
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)

    env = dict(spawner.environment)
    env["OPENAI_API_KEY"] = record["key"]
    env["JUPYTERHUB_USERNAME"] = username
    spawner.environment = env


c.Spawner.pre_spawn_hook = provision_llm_key

# ---------------------------------------------------------------------------
# Idle shutdown for the pilot
# ---------------------------------------------------------------------------
c.JupyterHub.services = [
    {
        "name": "idle-culler",
        "admin": True,
        "command": [
            "python",
            "-m",
            "jupyterhub_idle_culler",
            "--timeout=3600",
            "--cull-every=300",
            "--max-age=28800",
        ],
    }
]
