FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl nodejs npm \
    && npm install -g configurable-http-proxy \
    && pip install --no-cache-dir \
       jupyterhub==5.5.0 \
       dockerspawner==14.0.0 \
       jupyterhub-idle-culler \
       requests \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /srv/jupyterhub
COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]
