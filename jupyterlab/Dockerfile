# Dockerfile for JupyterLab
# Jupyterhub version: 3.1.1
# Date: 15.03.2023 DMY

FROM jupyter/scipy-notebook:2023-03-13

# JupyterHub Version
ARG JUPYTERHUB_VERSION=3.1.1

# Install packages
RUN pip3 install --no-cache \
    jupyterhub==$JUPYTERHUB_VERSION