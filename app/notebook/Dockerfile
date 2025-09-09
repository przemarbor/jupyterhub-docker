# Dockerfile for JupyterLab with C++ support
# JupyterHub version: 3.1.1

FROM jupyter/datascience-notebook:hub-3.1.1

# JupyterHub Version
ARG JUPYTERHUB_VERSION=3.1.1

USER root

RUN mkdir -p /home/jovyan/work/-my_public- && \
    chown jovyan:users /home/jovyan/work/-my_public-

RUN apt-get update && \
    apt-get install -y gnuplot octave wget curl && \
    apt-get clean

# Install Python packages
RUN pip3 install --no-cache \
    jupyterlab-language-pack-pl-PL \
    octave_kernel \
    jupyter-cpp-kernel

RUN apt-get update && \
    apt-get install -y libboost-all-dev && \
    apt-get clean

# Install requirements.txt file
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
# RUN pip install folium


# Ensure permissions and switch back to jovyan user
USER jovyan