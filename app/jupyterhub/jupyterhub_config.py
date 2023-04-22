# Configuration file for JupyterHub

# JupyterHub version: 3.1.1
# Dockerspawner version: 12.1.0
# JupyterHub CAS Authenticator version: 1.0.2

import os
import sys
from dockerspawner import DockerSpawner

c = get_config()

c.JupyterHub.active_server_limit = int(os.environ.get("ACTIVE_SERVER_LIMIT", 100))
c.JupyterHub.activity_resolution = int(os.environ.get("ACTIVITY_RESOLUTION", 300))
c.DockerSpawner.mem_limit = os.environ.get("MEM_LIMIT", "1G")
c.DockerSpawner.cpu_limit = int(os.environ.get("CPU_LIMIT", 1))
c.DockerSpawner.image = os.environ.get("DOCKER_NOTEBOOK_IMAGE", "notebook_img")
c.DockerSpawner.cmd = os.environ.get("DOCKER_SPAWN_CMD", "start-singleuser.sh")
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = os.environ.get("DOCKER_NETWORK_NAME")
c.DockerSpawner.remove = True # Remove containers once they are stopped
c.DockerSpawner.debug = False # For debugging arguments passed to spawned containers
c.JupyterHub.hub_ip = "jupyterhub" # User containers will access hub by container name on the Docker network
c.JupyterHub.hub_port = 9090
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret" # Persist hub data on volume mounted inside container
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"

notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR", "/home/jovyan")
c.DockerSpawner.notebook_dir = notebook_dir
appdata_dir = os.environ.get("APPDATA_DIR", "/data")

class MyDockerSpawner(DockerSpawner):
    def start(self):
        userName = self.user.name
        if "@prz.edu.pl" in userName:
            self.volumes = {appdata_dir + '/teachers/{}'.format(userName): notebook_dir,
                            appdata_dir + '/shared': {'bind': notebook_dir + '/shared', 'mode': 'rw'}}
        elif "@stud.prz.edu.pl" in userName:
            self.volumes = {appdata_dir + '/students/{}'.format(userName): notebook_dir,
                            appdata_dir + '/shared': {'bind': notebook_dir + '/shared', 'mode': 'ro'}}
        else:
            self.volumes = {appdata_dir + '/others/{}'.format(userName): notebook_dir,
                            appdata_dir + '/shared': {'bind': notebook_dir + '/shared', 'mode': 'ro'}}
        return super().start()

c.JupyterHub.spawner_class = MyDockerSpawner

# Administrator users
c.Authenticator.admin_users = {"166673@stud.prz.edu.pl"}

## Dummy Authenticator for testing only !!!
#c.JupyterHub.authenticator_class = "dummy"



## ----------------------------------------
## JupyterHub Cas Authenticator
# adapted config from GitHub cwaldbieser/jhub_cas_authenticator

c.JupyterHub.authenticator_class = 'jhub_cas_authenticator.cas_auth.CASAuthenticator'

# The CAS URL to redirect unauthenticated users to.
c.CASAuthenticator.cas_login_url = 'https://cas.prz.edu.pl/cas-server/login'
c.CASLocalAuthenticator.cas_logout_url = 'https://cas.prz.edu.pl/cas-server/logout'


# The service URL the CAS server will redirect the browser back to on successful authentication.
# If not set, this is set to the same URL the request comes in on.  This will work fine for
# simple deployments, but deployments behind a proxy or load banalncer will likely need to
# be adjusted so the CAS service redirects back to the *real* login URL for your Jupyterhub.
c.CASAuthenticator.cas_service_url = 'https://%s/hub/login' % os.environ['HOST']

# Path to CA certificates the CAS client will trust when validating a service ticket.
#c.CASAuthenticator.cas_client_ca_certs = '/path/to/ca_certs.pem'

# The CAS endpoint for validating service tickets.
c.CASAuthenticator.cas_service_validate_url = 'https://cas.prz.edu.pl/cas-server/serviceValidate'

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