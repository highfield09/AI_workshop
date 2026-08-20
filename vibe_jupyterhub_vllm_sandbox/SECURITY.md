# Security notes and limitations

## Intended scope

This Compose stack is for a small, trusted, single-host pilot. It demonstrates the request path and accounting model; it is not a hardened multi-tenant service.

## Credential hierarchy

There are three unrelated credential classes:

1. JupyterHub login credentials.
2. Per-user LiteLLM virtual API keys.
3. Private infrastructure secrets: LiteLLM master key and vLLM backend key.

Only class 2 enters a student container.

## Public exposure

The default Caddy edge publishes only `/v1` and `/v1/*`. It does not publish:

- LiteLLM key-management routes.
- LiteLLM administrative UI or usage administration.
- vLLM directly.
- JupyterHub.

vLLM stays on a Docker `internal: true` backend network with no host port. Its own API key is defence in depth, not the public security boundary.

## Sandbox-password warning

Each test username has a unique generated password, but the mapping is stored in the root-controlled Hub environment rather than an institutional identity provider. There is no MFA, lifecycle integration, or password-recovery workflow. Use institutional OAuth/OIDC before exposing JupyterHub beyond localhost/VPN.

## Docker socket warning

The JupyterHub container mounts `/var/run/docker.sock` so DockerSpawner can create student containers. Control of that socket is effectively control of the Docker host. Only the Hub container and trusted administrators should have access. Never mount it in student containers.

## Student-container isolation

The sandbox:

- Drops Linux capabilities.
- Enables `no-new-privileges`.
- Sets CPU, memory and process limits.
- Gives each user a separate persistent Docker volume.
- Mounts course material read-only.

Remaining limitations:

- Student containers share one Docker network and are not protected by Kubernetes NetworkPolicy.
- Internet egress is unrestricted.
- Container names and network services may be discoverable.
- Docker/host kernel vulnerabilities are outside this sandbox's isolation guarantees.
- Students can run arbitrary Python, R and shell commands in their own containers.

Do not mount sensitive host directories or credentials into student containers.

## Student virtual keys

A virtual key is created once per username and cached in plaintext in `/srv/jupyterhub/student_keys.json` inside the root-controlled Hub state volume. It is then injected as an environment variable into the student's container.

Consequences:

- The user can read and export their own key.
- The key can be used from another client until it expires or is revoked.
- Requests remain attributable to the key/user and retain its model/rate limits.
- A copied key is a bearer credential; identity does not follow it cryptographically.

For production, prefer short-lived identity-bound tokens, OIDC token exchange, or a gateway plugin that validates JupyterHub-issued identity rather than storing long-lived bearer keys.

## Prompt and response logging

This stack enables LiteLLM spend/usage records. It does not intentionally add a callback that stores full prompt and response bodies. Reverse-proxy access logs may contain paths, status codes and request metadata but should not contain Authorization headers.

Review the exact LiteLLM image/version and logging configuration before using confidential data. Define retention and deletion policies. Avoid personal, clinical, unpublished or otherwise sensitive datasets in this pilot.

## Browser and network tools

Headless Chromium is disabled by default. Enabling it increases the attack surface and allows students or agents to interact with arbitrary web content. Browser agents should run in more restricted disposable containers with destination controls.

## Rate limits are not total compute isolation

RPM, TPM and parallel-request limits reduce abuse but do not fully protect GPU service availability. Also configure:

- vLLM maximum model length.
- Maximum output tokens.
- Maximum active sequences.
- Gateway request-body limits.
- Per-user notebook CPU/RAM limits.
- Service monitoring and emergency key revocation.

## Required production improvements

- Individual institutional authentication.
- TLS and secure headers for all public services.
- WAF or institutional reverse proxy.
- Per-user network isolation.
- Restricted egress and package mirrors.
- Central secret manager and key rotation.
- Backups and restore tests.
- Pinned image digests rather than mutable `latest` tags.
- Vulnerability and dependency scanning.
- Audit-log access controls.
- Formal acceptable-use and data-retention policies.
