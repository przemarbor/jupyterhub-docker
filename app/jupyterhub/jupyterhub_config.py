#Configuration file for JupyterHub

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
c.DockerSpawner.debug = True # For debugging arguments passed to spawned containers
c.JupyterHub.hub_ip = "jupyterhub" # User containers will access hub by container name on the Docker network
c.JupyterHub.hub_port = 9090
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret" # Persist hub data on volume mounted inside container
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"

def is_six_digits_username(username):
    return username[:6].isdigit() and len(username) >= 6


# ======================
# KONFIGURACJA WOLUMENÓW Z WIZUALIZACJĄ
# ======================

def setup_user_environment(spawner):
    """Ustawia zmienne środowiskowe, volumes i komendę post-start"""
    username = spawner.user.name
    
    # Normalizuj nazwę użytkownika dla wolumenów Dockera
    safe_username = username.replace('@', '-').replace('.', '-')
    if safe_username.endswith('-stud-prz-edu-pl'):
        safe_username = safe_username[:-len('-stud-prz-edu-pl')]
    elif safe_username.endswith('-prz-edu-pl'):
        safe_username = safe_username[:-len('-prz-edu-pl')]
    
    notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR", "/home/jovyan/work")
    my_public_dir = "/home/jovyan/work/-my_public-"
    public_dir = "/home/jovyan/public"
    readme_dir = "/home/jovyan/-README-"

    volumes = {
        f"jupyterhub-user-{safe_username}-work": {"bind": notebook_dir, "mode": "rw"},
        "jupyterhub-public": {"bind": public_dir, "mode": "ro"},
        "readme_dir": {"bind": readme_dir, "mode": "ro"}
    }

    environment = {}

    if not is_six_digits_username(username):
        volumes[f"jupyterhub-user-{safe_username}-my_public"] = {"bind": my_public_dir, "mode": "rw"}
        environment["JUPYTERHUB_MY_PUBLIC_VOLUME"] = "true"
    else:
        environment["JUPYTERHUB_MY_PUBLIC_VOLUME"] = "false"
        spawner.post_start_cmd = f"""
        /bin/bash -c '
        if [ -d {my_public_dir} ]; then
            rm -rf {my_public_dir}
        fi
        '
        """

    spawner.volumes = volumes
    spawner.environment = environment

c.Spawner.pre_spawn_hook = setup_user_environment

c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"


debug = os.environ.get("DEBUG", "False")
if debug == "True":
    c.Authenticator.admin_users = {"admin"}
    c.JupyterHub.authenticator_class = "dummy"
    c.DockerSpawner.debug = True
else:
    c.Authenticator.admin_users = {"admin"} # this line needs to be modified in configuration
    c.JupyterHub.authenticator_class = 'jhub_cas_authenticator.cas_auth.CASAuthenticator'
    c.CASAuthenticator.cas_login_url = 'https://cas.prz.edu.pl/cas/login'
    c.CASAuthenticator.cas_logout_url = 'https://cas.prz.edu.pl/cas/logout'
    c.CASAuthenticator.cas_service_url = 'https://%s/hub/login' % os.environ['HOST']
    c.CASAuthenticator.cas_service_validate_url = 'https://cas.prz.edu.pl/cas/serviceValidate'
    #c.CASAuthenticator.cas_required_attribs = {('memberOf', 'jupyterhub_users')}


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
