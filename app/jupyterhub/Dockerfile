# Dockerfile for JupyterHub
# JupyterHub version: 3.1.1

FROM jupyterhub/jupyterhub:3.1.1

# Install packages
RUN pip install \
    # Dockerspawner for JupyterHub
    dockerspawner==12.1.0 \
    # JupyterHub CAS Authenticator
    jhub_cas_authenticator==1.0.2 \
    # JupyterHub Idle Culler
    jupyterhub-idle-culler==1.2.1

# Copy configuration file
COPY ./jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]