# JupyterHub - Docker

## Introduction
This project implements a JupyterHub environment using Docker containers, the Traefik server as a reverse proxy, and various authentication and user management mechanisms. The system is defined in the `docker-compose.yml`, `Dockerfile`, `jupyterhub_config.py`, and `jupyterhub_config_test.py` files.

## Configuration and Launch


### Initial Configuration
Before the first launch, the environment must be configured, mainly by editing the `.env` file.

- **Host Address**: Change the value of the `HOST` environment variable in the `.env` file to the address where JupyterHub will be accessible (e.g., `HOST=jupyterhub.prz.edu.pl`).

- **Email Address**: Edit the administrator email address in the `traefik.yml` file. It is used for generating a TLS certificate via Let's Encrypt.

- **Administrator Setup**: In the `jupyterhub_config.py` file, add the administrator's email address to the `c.Authenticator.admin_users` variable.

- ~~Additionally, TLS certificates needed to be uploaded to `/app/proxy/certs/` *(using file names: cert-host-key.pem and cert-host.pem)*.~~

**Note**: Uploading TLS certificates to `/app/proxy/certs/` is no longer required, as Traefik automatically generates certificates via Let's Encrypt.



### Launch
To start the project, use the appropriate docker-compose.yml files depending on the environment you need.

#### Production Environment
To run the production server, use the command:

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```
The services are available at https://{HOST} (e.g., https://jupyterhub.prz.edu.pl
).

#### Test Environment

To start the test server (independent of production), run:

```bash
docker-compose -f docker-compose.test.yml up -d --build
```

The test version is available on port 8443 at https://{HOST}:8443/test/.

By default, port 80 (HTTP) is disabled, and traffic is redirected to port 443 (HTTPS).


## Main Features

### 1. User Container Management
* **Dockerspawner**: Creates individual Jupyter Notebook instances for each user.
* **Resource Limits**: Memory (`MEM_LIMIT`) and CPU (`CPU_LIMIT`) limits are dynamically configured.
* **Volume Management**:
    * Private volume for each user.
    * Public volume for shared resources.

### 2. Authentication
* **CAS Authenticator**: Integration with the CAS authentication system.
* **Dummy Authenticator**: Test mode for local development.

### 3. Idle Culler
Automatically shuts down inactive sessions after a specified period.

### 4. Reverse Proxy (Traefik)
* Automatic SSL certificate management.
* Endpoint configuration.

---

## Detailed Volume Access Specification

### 1. Private Volume (`/home/jovyan/work`)
* **Purpose**: 
  * User workspace
  * Private data and configurations
  * Host path: `/var/lib/docker/volumes/jupyterhub-user-<username>-work/_data`

### Public Volume (`/home/jovyan/public`)
* **Access for all users**:
    * Read-only
    * No write permissions
    * Host path: `/var/lib/docker/volumes/jupyterhub-public/_data`

### `my_public` Volume (instructors only)
* **Operation**:
    * Automatically copies files from `my_public` to the public folder on the host.
    * Implemented via a script monitoring changes with `inotifywait`.
* **Access**:
    * Only instructors (users without a 6-digit ID) have read-write access.
    * Students do not have access.

### Information Volume (`/home/jovyan/-README-`)
* **Access for all users**:
    * Read-only
    * No write permissions
    * Host path: `/var/lib/docker/volumes/readme_dir/_data`

### Actual Permissions:
| Volume | Students (6-digit ID) | Instructors (other IDs) |
| :--- | :---: | :---: |
| `work` | Read-Write | Read-Write |
| `public` | Read-only | Read-only |
| `my_public` | No access | Read-Write |
| `-README-` | Read-only | Read-only |

---

## Public Folder Workaround
The system uses a mechanism to copy files from `my_public` to the public folder on the host because:
1. Docker Volumes have limitations in managing permissions.
2. Direct writes to the public volume caused synchronization issues.
3. This solution ensures that only approved instructor files reach the public space.

---

# Project Status

### Project
- [x] Prepare `docker-compose.yml`
- [x] Organize project structure
- [x] Separate configuration for development and production
- [x] Configure environment variables

### JupyterHub
- [x] Resolve permission issues
- [x] Setup CAS authentication
- [ ] Implement course management system

### Notebook
- [x] Fix permission issues when creating a new notebook
- [x] Add Julia and R kernels
- [x] Add C++ support
- [x] Prepare Python packages file
- [ ] Add Maxima kernel

### Proxy
- [x] Prepare `traefik.yml`
- [x] Add HTTPS support
- [x] Configure certificates
- [x] Automatic certificate generation

## Notes
The current version includes all main features described in the documentation. Ongoing development includes:
* Course management system
* Additional programming languages
* Improved resource monitoring

## Repository Structure

```
JupyterHub
.
├── .env
├── README.md
├── docker-compose.prod.yml
├── docker-compose.test.yml
├── app
│   ├── jupyterhub
│   │   ├── Dockerfile
│   │   ├── jupyterhub_config.py
│   │   └── jupyterhub_config_test.py
│   ├── jupyterlab
│	│	├── requirements.txt
│   │   └── Dockerfile
│   └── proxy
│       ├── Dockerfile
│       └── traefik.yml

```


# Documentation

## 1. JupyterHub
Version: jupyterhub/jupyterhub:3.1.1

*(Located in /app/jupyterhub/Dockerfile and configuration in /app/jupyterhub/jupyterhub_config.py)*

[JupyterHub config file](https://github.com/jupyterhub/jupyterhub-deploy-docker)

## 2. Proxy
Version: traefik:v2.9

TLS configuration file must be separate; in this case, it is tls.yml

*(Located in /app/proxy/Dockerfile and configuration in /app/proxy/traefik.yml)*

[Traefik documentation](https://doc.traefik.io/traefik/)

[Traefik config entry points](https://doc.traefik.io/traefik/routing/entrypoints/)

## 3. Notebook
Version: jupyter/scipy-notebook:hub-3.1.1

*(Located in /app/jupyterlab/Dockerfile)*

[Building Docker image for Jupyter Notebook](https://jupyterhub-dockerspawner.readthedocs.io/en/latest/docker-image.html)

[Datascience-notebook](https://hub.docker.com/r/jupyter/datascience-notebook/tags/)

## 4. JHubAuthenticators - CAS Authentication
Version: jhubauthenticators==1.0.2

*(Located in /app/jupyterhub/Dockerfile and configuration in /app/jupyterhub/jupyterhub_config.py)*

[CAS authenticator](https://github.com/cwaldbieser/jhub_cas_authenticator)

## 5. JupyterHub Idle Culler Service
Version 1.2.1

*(Located in /app/jupyterhub/Dockerfile and configuration in /app/jupyterhub/jupyterhub_config.py)*

[JupyterHub Idle Culler Service](https://github.com/jupyterhub/jupyterhub-idle-culler)

## 6. Docker-compose with Let's Encrypt: TLS Challenge
Configuration for automatic TLS certificate generation using Let's Encrypt.

[Docker-compose with Let's Encrypt: TLS Challenge](https://doc.traefik.io/traefik/user-guides/docker-compose/acme-tls/)
