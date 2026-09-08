ARG BASE_IMAGE=quay.io/jupyter/datascience-notebook:latest
FROM ${BASE_IMAGE}

ARG INSTALL_BROWSER=0

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl \
       git \
       jq \
       procps \
       unzip \
       build-essential \
    && if [ "${INSTALL_BROWSER}" = "1" ]; then \
         apt-get install -y --no-install-recommends chromium chromium-driver; \
       fi \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER ${NB_UID}

RUN python -m pip install --no-cache-dir --upgrade \
      jupyterhub==5.5.0 \
      jupyter-ai==3.0.1 \
      jupyter-ai-tools==0.6.0 \
      jupyter-server-proxy \
      openai \
      httpx \
      python-dotenv \
      biopython \
      polars \
      plotly \
      openpyxl \
      streamlit \
      pytest

RUN if [ "${INSTALL_BROWSER}" = "1" ]; then \
      python -m pip install --no-cache-dir playwright; \
    fi

WORKDIR /home/jovyan/work
