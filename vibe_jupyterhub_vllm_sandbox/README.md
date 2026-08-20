# JupyterHub + Qwen3.5-9B + Secure LLM Gateway Sandbox

A single-Linux-host classroom sandbox that provides:

- JupyterHub with one Docker container and persistent workspace per user.
- Python, R, Bash, Git, common biology/data packages, Jupyter AI, Streamlit and optional Chromium.
- Qwen3.5-9B served by vLLM on **physical CUDA device 0**.
- LiteLLM as the authenticated OpenAI-compatible gateway and usage ledger.
- One revocable, rate-limited virtual API key per JupyterHub username.
- Caddy as a route allow-list: only `/v1` and `/v1/*` can reach LiteLLM.
- An optional public HTTPS endpoint for the LLM API; raw vLLM is never published.

This is a **small trusted-workshop sandbox**, not a finished production deployment.
Read [SECURITY.md](SECURITY.md) before allowing remote users.

## Architecture

```text
Browser
  -> JupyterHub on localhost/VPN
      -> DockerSpawner
          -> isolated student notebook container
              -> http://api-proxy:8080/v1
                  -> Caddy route allow-list
                      -> LiteLLM virtual-key gateway + PostgreSQL usage logs
                          -> private backend network
                              -> vLLM on GPU 0

External API client (optional)
  -> https://llm.example.edu/v1
      -> public Caddy edge
          -> LiteLLM
              -> private vLLM
```

## What a student can access

Inside their own container, a student receives:

- A persistent `/home/jovyan/work` volume.
- Read-only `/home/jovyan/course_materials`.
- Python and R kernels plus a Bash terminal.
- Their own `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_API_BASE`, and `CLASSROOM_MODEL` environment variables.
- The public/private gateway API permitted by that key.
- Internet egress from the container in this simple sandbox.

They do **not** receive:

- The LiteLLM master key.
- The private vLLM backend key.
- A host Docker socket.
- The model files.
- Another student's persistent volume.
- A host-published vLLM port.

A student can read and copy their own virtual key. That is intentional: it allows testing an external client through the same quota. Treat the key as a password and revoke it if exposed.

## Model and initial limits

The defaults point to:

```text
/home/highfieldc/LLM_Lab/cache/hub/
  models--Qwen--Qwen3.5-9B/
  snapshots/c202236235762e1c871ad0ccb60c8ee5ba337b9a
```

The repository root is mounted rather than only the snapshot because Hugging Face snapshots commonly contain symlinks into the repository's `blobs` directory.

Initial vLLM settings are conservative for one RTX A5000 24 GB:

- GPU: device `0` only.
- Text-only model loading.
- Maximum model context: 8,192 tokens.
- Gateway-advertised maximum input: 7,168 tokens.
- Maximum output: 1,024 tokens.
- Maximum active sequences: 4.
- Maximum CUDA graph capture size: 8.
- GPU memory utilisation target: 0.88.
- Prefix caching enabled.
- Thinking disabled by default for predictable classroom latency.

These are starting settings, not measured throughput guarantees. Load-test before a synchronous class.

## Prerequisites

On the Linux host:

1. NVIDIA driver working with `nvidia-smi`.
2. Docker Engine.
3. Docker Compose v2 (`docker compose`).
4. NVIDIA Container Toolkit configured for Docker.
5. The stated local model directory readable by Docker.
6. Free host ports 8000 and 4000 for local mode.
7. For public HTTPS: a DNS record plus inbound TCP 80 and 443.

A useful GPU-container check is:

```bash
docker run --rm --gpus '"device=0"' \
  nvidia/cuda:12.9.1-base-ubuntu24.04 nvidia-smi
```

The container carries its own CUDA userspace. The host's installed CUDA toolkit is less important than a compatible NVIDIA driver and a working NVIDIA Container Toolkit.

## 1. Copy and initialise

```bash
cd /path/to/vibe_jupyterhub_vllm_sandbox
./scripts/generate_secrets.sh
chmod 600 .env
```

The script creates independent secrets for:

- Unique per-user JupyterHub logins.
- JupyterHub cookie signing.
- LiteLLM administration.
- LiteLLM key encryption/salting.
- The private vLLM backend.
- PostgreSQL.

Inspect `.env`. At minimum, verify the model path and allowed usernames:

```dotenv
QWEN_MODEL_ROOT=/home/highfieldc/LLM_Lab/cache/hub/models--Qwen--Qwen3.5-9B
QWEN_SNAPSHOT_ID=c202236235762e1c871ad0ccb60c8ee5ba337b9a
JUPYTERHUB_ALLOWED_USERS=instructor,student1,student2
JUPYTERHUB_ADMIN_USERS=instructor
```

## 2. Preflight checks

```bash
./scripts/doctor.sh
```

This checks Docker, Compose, the model path, `nvidia-smi`, and Compose rendering.

## 3. Build the classroom images

```bash
./scripts/build.sh
```

To include headless Chromium in every user image, set this before building:

```dotenv
INSTALL_BROWSER=1
```

For the first sandbox, leave it disabled.

## 4. Start locally

```bash
./scripts/up_local.sh
```

Monitor the model and gateway:

```bash
docker compose logs -f vllm
docker compose logs -f litellm
docker compose ps
./scripts/status.sh
```

Local endpoints:

- JupyterHub: `http://127.0.0.1:8000`
- OpenAI-compatible API: `http://127.0.0.1:4000/v1`

If working from another machine, use SSH forwarding rather than publishing the sandbox Hub:

```bash
ssh -L 8000:127.0.0.1:8000 \
    -L 4000:127.0.0.1:4000 \
    highfieldc@YOUR_HOST
```

Then open `http://127.0.0.1:8000` locally.

## 5. Log in as test users

The generated `.env` contains:

```dotenv
JUPYTERHUB_USER_PASSWORDS_JSON='sys-generated JSON mapping'
```

- Every allowed username receives a different generated password.
- View them locally with `./scripts/show_login_credentials.sh`.

Starting a user's server triggers JupyterHub's pre-spawn hook. It creates a LiteLLM virtual key with that username as `user_id`, stores it in the Hub's root-controlled state volume, and injects it into only that user's container.

**Important:** passwords are stored as plaintext configuration inside the root-controlled Hub container for this sandbox. Use institutional SSO/OIDC for a real class.

## 6. Test inside Jupyter

Open the read-only notebook:

```text
/home/jovyan/course_materials/01_gateway_test.ipynb
```

Copy it into `/home/jovyan/work`, then run it. It tests:

- Environment variables.
- `/v1/models` access.
- Chat completion through the gateway.
- Token usage returned in the response.
- A small Python coding task.

The equivalent Python client is:

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url=os.environ["OPENAI_BASE_URL"],
    api_key=os.environ["OPENAI_API_KEY"],
)

response = client.chat.completions.create(
    model=os.environ.get("CLASSROOM_MODEL", "classroom-qwen"),
    messages=[
        {"role": "system", "content": "You are a concise biology coding tutor."},
        {"role": "user", "content": "Write a GC percentage function in Python."},
    ],
    max_tokens=256,
    temperature=0.2,
)
print(response.choices[0].message.content)
print(response.usage)
```

## 7. Inspect a student's key and test externally

For sandbox administration only:

```bash
./scripts/show_student_keys.sh
```

Copy the key for `student1`, then test the localhost gateway:

```bash
export OPENAI_API_KEY='sk-...'
./scripts/test_gateway.sh
```

Or use curl directly:

```bash
curl http://127.0.0.1:4000/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "classroom-qwen",
    "messages": [{"role":"user","content":"Return the word READY."}],
    "max_tokens": 32
  }'
```

The same virtual key works from an approved external client when public HTTPS is enabled. RPM, TPM, model access and parallel-request restrictions remain attached to the key.

## 8. View token and request usage

Per-user summary from LiteLLM:

```bash
./scripts/show_usage.sh student1
```

Aggregated database report:

```bash
./scripts/token_report.sh
```

To revoke a leaked or retired student key, first stop that user's notebook server, then run:

```bash
./scripts/revoke_student_key.sh student1
```

The next spawn creates a fresh key with the current `.env` limits.

The default report groups:

- Request count.
- Input tokens.
- Output tokens.
- Total tokens.
- Average request duration.
- Last request time.

The model is configured with zero monetary token cost, so this is a compute/usage ledger rather than vendor billing.

## 9. Confirm the security boundary

```bash
./scripts/security_smoke_test.sh
```

It checks that:

- `/key/generate` is not exposed by the student/public proxy.
- Unauthenticated inference is rejected.
- Raw vLLM has no host-published port.
- vLLM is attached only to the internal backend network.

## 10. Enable a public HTTPS API

Do not publish the JupyterHub login from this sandbox. The supplied public profile exposes only `/v1` API routes.

Create a DNS A/AAAA record, for example:

```text
llm.yourdomain.edu -> public IP of the gateway host
```

Set:

```dotenv
LLM_DOMAIN=llm.yourdomain.edu
ACME_EMAIL=admin@yourdomain.edu
```

Allow inbound TCP 80/443 and start:

```bash
./scripts/up_public.sh
```

Test from an external machine:

```bash
export OPENAI_API_KEY='student-virtual-key'
./scripts/test_gateway.sh https://llm.yourdomain.edu/v1
```

The edge deliberately returns `404` for LiteLLM administrative routes. Only `/v1` and `/v1/*` are forwarded.

## 11. Change student quotas

Edit `.env` before first provisioning:

```dotenv
STUDENT_RPM_LIMIT=6
STUDENT_TPM_LIMIT=12000
STUDENT_MAX_PARALLEL_REQUESTS=1
STUDENT_KEY_DURATION=30d
```

These limits are copied into each key when it is created. Changing `.env` does not retroactively update an existing virtual key. For the sandbox, remove/revoke the existing key through LiteLLM administration or reset the Hub and gateway state before re-provisioning.

## 12. Stop the sandbox

```bash
./scripts/down.sh
```

This stops containers but retains named volumes. To destroy all student work, Hub state, keys and LiteLLM usage records:

```bash
docker compose --profile public down -v
```

That command is destructive.

## Suggested first load test

1. Start `student1` and `student2` servers.
2. Confirm each receives a different virtual key.
3. Run one 128-token request from each user.
4. Start two requests at once under the **same** student key; the parallel limit should reject or queue the excess according to LiteLLM behaviour.
5. Exceed six requests within a minute and confirm rate limiting.
6. Run `scripts/token_report.sh`.
7. Observe GPU 0 with:

```bash
watch -n 1 nvidia-smi -i 0
```

8. Increase `VLLM_MAX_NUM_SEQS` only after measuring memory and latency.

## Production migration path

Before a real public class:

- Replace the sandbox password authenticator with institutional OIDC/OAuth.
- Move from DockerSpawner to KubeSpawner where NetworkPolicy can isolate students.
- Remove the Docker socket from the Hub by using a more strongly isolated control plane.
- Use short-lived identity-bound gateway tokens or a secret manager.
- Add outbound egress policy and internal package mirrors.
- Put Hub and gateway behind an institutional WAF/reverse proxy.
- Add Redis if required for scaled LiteLLM rate limiting.
- Define prompt-content retention and student-consent policies.
- Add monitoring, alerting, backups and key revocation procedures.
- Run a concurrency test matching the expected whole class.
