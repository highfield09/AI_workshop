# Vibe Coding Classroom Sandbox

This directory is mounted read-only in every student workspace.

Copy the starter notebook into your writable `work` directory before editing:

```bash
cp /home/jovyan/course_materials/01_gateway_test.ipynb /home/jovyan/work/
```

The following environment variables are already present in each Jupyter server:

- `OPENAI_BASE_URL`: the allow-listed classroom gateway endpoint
- `OPENAI_API_KEY`: a unique revocable virtual key for the current JupyterHub user
- `CLASSROOM_MODEL`: the model alias exposed to students
- `JUPYTERHUB_USERNAME`: the authenticated username

The key can also be used from an external client after the instructor enables the
public HTTPS endpoint. Treat it as a password and do not commit it to notebooks,
Git repositories, screenshots, or shared files.
