# JupyterHub on Docker
This is updated version of ["*JupyterHub deployment in use at Université de Versailles*"](https://github.com/defeo/jupyterhub-docker).

## Run
> docker-compose build
> 
> docker-compose run


## Todo
### Docker-compose
- [x] Recreate docker-compose.yml
### JupyterHub
- [x] Prepare for CAS authentication
- [x] Prepare jupyterhub_config.py
- [ ] Fix not using allowed_users
### Traefik
- [x] Prepare traefik.toml
- [x] Add HTTPS
- [x] Configure redirect
- [x] Prepare certificates
### Jupyterlab
- [x] Repair issuficient permissions while creating new notebook
- [ ] Change user name in container (!whoami)
- [ ] Add custom logo
- [ ] Add python packages
- [ ] Remove notifications
- [ ] Remove widgets
- [x] Add Julia kernel
- [x] Add R kernel
- [ ] Add c++ kernel

## Repository structure
```
JupyterHub
├── .env
├── README.md
├── docker-compose.yml
├── jupyterhub
│   ├── Dockerfile
│   └── jupyterhub_config.py
├── jupyterlab
│   └── Dockerfile
└── traefik
    ├── tls.yml
    ├── localhost-key.pem
    ├── localhost.pem
    └── traefik.toml
```


### 1. Traefik - Reverse proxy
Version: traefik:v2.9 (Docker-compose)

[Traefik documentation](https://doc.traefik.io/traefik/)
[Traefik config Entry Poionts](https://doc.traefik.io/traefik/routing/entrypoints/)

The TLS configuration shuld be in separate file (tls.yml) and mounted to traefik container, in config file (traefik.yml) it is included in providers section.

### 2. JupyterHub
Version: jupyterhub/jupyterhub:3.1.1 (JupyterHub Dockerfile, config in jupyterhub_config.py)

[Jupyterhub config](https://github.com/jupyterhub/jupyterhub-deploy-docker)

#### 2.1 DockerSpawner
Version: dockerspawner==12.1.0 (pip install in JupyterHub Dockerfile, config in jupyterhub_config.py)

[DockerSpawner install](https://jupyterhub-dockerspawner.readthedocs.io/en/latest/install.html)

### 3. Jupyterlab - Jupyter notebook
Version: jupyter/scipy-notebook:hub-3.1.1 (Jupyterlab Dockerfile)

[Building Docker image for Jupyter Notebook](https://jupyterhub-dockerspawner.readthedocs.io/en/latest/docker-image.html)

[Datascience-notebook](https://hub.docker.com/r/jupyter/datascience-notebook/tags/)


### 4. Jhubauthenticators - CAS authentication
Version: jhubauthenticators==1.0.2 (pip install in JupyterHub Dockerfile, config in jupyterhub_config.py)

[CAS authenticator](https://github.com/cwaldbieser/jhub_cas_authenticator)


### 5. JupyterHub Idle Culler Service
Version: 1.2.1 (pip install in JupyterHub Dockerfile, config in jupyterhub_config.py)

[JupyterHub Idle Culler Service](https://github.com/jupyterhub/jupyterhub-idle-culler)


### 6. JupyterHub Traefik Proxy
Version: 0.3.0

[Installation](https://jupyterhub-traefik-proxy.readthedocs.io/en/latest/install.html)
[JupyterHub Traefik Proxy PyPI](https://pypi.org/project/jupyterhub-traefik-proxy/)
[JupyterHub Traefik Proxy](https://github.com/jupyterhub/traefik-proxy)