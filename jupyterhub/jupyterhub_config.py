# Configuration file for JupyterHub
# Date: 15.03.2023 DMY

# JupyterHub version: 3.1.1
# Dockerspawner version: 12.1.0
# JupyterHub CAS Authenticator version: 1.0.2

import os
import sys

c = get_config()


# Maximum number of concurrent servers that can be active at a time
c.JupyterHub.active_server_limit = 100

# Resolution (in seconds) for updating activity
c.JupyterHub.activity_resolution = 300

# The base URL of the entire application
c.JupyterHub.base_url = "/"

# If person can have more than one server, then he can change the name of the server
c.JupyterHub.allow_named_servers = True

# Configure more than one server for admins
def named_server_limit_per_user_fn(handler):
    user = handler.current_user
    if user and user.admin:
        return 5
    return 1

c.JupyterHub.named_server_limit_per_user = named_server_limit_per_user_fn

c.DockerSpawner.mem_limit = "2G"

c.DockerSpawner.cpu_limit = 2





# ----------------------------------------
# Dockerspawner
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
c.DockerSpawner.image = os.environ["DOCKER_NOTEBOOK_IMAGE"]

spawn_cmd = os.environ.get("DOCKER_SPAWN_CMD", "start-singleuser.sh")
c.DockerSpawner.cmd = spawn_cmd

# Connect containers to this Docker network
network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Notebook directory
notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR") or "/home/jovyan"
c.DockerSpawner.notebook_dir = notebook_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {"/Users/jakub/Repos/jupyterhub-docker/data" + "/hub-{username}": notebook_dir}

# Remove containers once they are stopped
c.DockerSpawner.remove = True

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = 9090

# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"
# ----------------------------------------



# Administrator users
c.Authenticator.admin_users = {"admin"}


## Dummy Authenticator for testing only !!!
c.JupyterHub.authenticator_class = "dummy"

## ----------------------------------------
## JupyterHub Cas Authenticator
# adapted config from GitHub cwaldbieser/jhub_cas_authenticator

#c.JupyterHub.authenticator_class = 'jhub_cas_authenticator.cas_auth.CASAuthenticator'

# The CAS URL to redirect unauthenticated users to.
#c.CASAuthenticator.cas_login_url = 'https://cas.prz.edu.pl/cas-server/login'
#c.CASLocalAuthenticator.cas_logout_url = 'https://cas.prz.edu.pl/cas-server/logout'


# The service URL the CAS server will redirect the browser back to on successful authentication.
# If not set, this is set to the same URL the request comes in on.  This will work fine for
# simple deployments, but deployments behind a proxy or load banalncer will likely need to
# be adjusted so the CAS service redirects back to the *real* login URL for your Jupyterhub.
#c.CASAuthenticator.cas_service_url = 'https://%s/hub/login' % os.environ['HOST']
#c.CASAuthenticator.cas_service_url = 'https://test1234.prz.edu.pl'

# Path to CA certificates the CAS client will trust when validating a service ticket.
#c.CASAuthenticator.cas_client_ca_certs = '/path/to/ca_certs.pem'

# The CAS endpoint for validating service tickets.
#c.CASAuthenticator.cas_service_validate_url = 'https://cas.prz.edu.pl/cas-server/serviceValidate'

# A set of attribute name and value tuples a user must have to be allowed access.
#c.CASAuthenticator.cas_required_attribs = {('memberOf', 'jupyterhub_users')}
## ----------------------------------------


## ----------------------------------------
# JupyterHub Idle Culler
# adapted config from GitHub jupyterhub/jupyterhub-idle-culler

c.JupyterHub.load_roles = [
    {
        "name": "jupyterhub-idle-culler-role",
        "scopes": [
            "list:users",
            "read:users:activity",
            "read:servers",
            "delete:servers",
            # "admin:users", # if using --cull-users
        ],
        # assignment of role's permissions to:
        "services": ["jupyterhub-idle-culler-service"],
    }
]

c.JupyterHub.services = [
    {
        "name": "jupyterhub-idle-culler-service",
        "command": [
            sys.executable,
            "-m", "jupyterhub_idle_culler",
            "--timeout={0}".format(os.environ.get("JUPYTERHUB_IDLE_CULLER_TIMEOUT", "3600")),
        ],
    }
]

## ----------------------------------------