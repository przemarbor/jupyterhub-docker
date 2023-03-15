# JupyterHub on Docker
This is updated version of ["*JupyterHub deployment in use at Université de Versailles*"](https://github.com/defeo/jupyterhub-docker).

## Run
> docker-compose build
> 
> docker-compose run


## Todo
### Docker-compose
- [ ] Recreate docker-compose.yml
### JupyterHub
- [ ] Prepare for CAS authentication
- [ ] Prepare jupyterhub_config.py
### Traefik
- [ ] Prepare traefik.toml
- [ ] Add HTTPS
- [ ] Configure redirect
- [ ] Prepare certificates
### Jupyterlab
- [ ] Repair issuficient permissions while creating new notebook

## Repository structure
```
JupyterHub
├── README.md
├── docker-compose.yml
├── jupyterhub
│   ├── Dockerfile
│   └── jupyterhub_config.py
├── jupyterlab
│   └── Dockerfile
└── traefik
    └── traefik.toml
```


### 1. Traefik - Reverse proxy
Version: traefik:v2.9 (Docker-compose)

[Traefik documentation](https://doc.traefik.io/traefik/)

### 2. JupyterHub
Version: jupyterhub/jupyterhub:3 (JupyterHub Dockerfile)

https://github.com/jupyterhub/jupyterhub-deploy-docker/blob/master/jupyterhub_config.py

#### 2.1 DockerSpawner
Version: dockerspawner==12.1.0 (pip install in JupyterHub Dockerfile)

https://jupyterhub-dockerspawner.readthedocs.io/en/latest/install.html

### 3. Jupyterlab - Jupyter notebook
Version: jupyter/scipy-notebook:hub-3.1.1 (Jupyterlab Dockerfile)

https://hub.docker.com/r/jupyter/scipy-notebook/tags



