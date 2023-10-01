# Dockerfile for JupyterLab
# Jupyterhub version: 3.1.1

FROM jupyter/datascience-notebook:hub-3.1.1

# JupyterHub Version
ARG JUPYTERHUB_VERSION=3.1.1

USER root
RUN apt-get update && \
    apt-get install -y gnuplot octave && \
    apt-get clean

# Install packages
RUN pip3 install --no-cache \
    jupyterlab-language-pack-pl-PL \
    octave_kernel && \
    export OCTAVE_EXECUTABLE=$(which octave)

USER jovyan
