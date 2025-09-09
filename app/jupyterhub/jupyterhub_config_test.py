# Plik konfiguracyjny JupyterHub dla wersji testowej
# Wersja testowa z DummyAuthenticator do celów testowych

import os
import sys
import json
from dockerspawner import DockerSpawner
import subprocess


c = get_config()

# Ustawienia limitów aktywności
c.JupyterHub.active_server_limit = int(os.environ.get("ACTIVE_SERVER_LIMIT", 100))
c.JupyterHub.activity_resolution = int(os.environ.get("ACTIVITY_RESOLUTION", 300))

# Ustawienia dla DockerSpawner
c.DockerSpawner.mem_limit = os.environ.get("MEM_LIMIT", "1G")
c.DockerSpawner.cpu_limit = int(os.environ.get("CPU_LIMIT", 1))
c.DockerSpawner.image = os.environ.get("DOCKER_NOTEBOOK_IMAGE", "notebook_img")
c.DockerSpawner.cmd = os.environ.get("DOCKER_SPAWN_CMD", "start-singleuser.sh")
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = os.environ.get("DOCKER_NETWORK_NAME")
c.DockerSpawner.remove = True  # Usuwanie kontenerów po zakończeniu pracy
c.DockerSpawner.debug = True  # Ustawienia debugowania

# Ustawienia adresu JupyterHub
c.JupyterHub.base_url = '/test/'
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = 9090
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"  # Lokalizacja pliku cookie
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"

def is_six_digits_username(username):
    return username[:6].isdigit() and len(username) >= 6

# ======================
# KONFIGURACJA WOLUMENÓW Z WIZUALIZACJĄ
# ======================
def setup_user_environment(spawner):
    username = spawner.user.name
    safe_username = username.replace('@', '-').replace('.', '-')
    
    if safe_username.endswith('-stud-prz-edu-pl'):
        safe_username = safe_username[:-len('-stud-prz-edu-pl')]
    elif safe_username.endswith('-prz-edu-pl'):
        safe_username = safe_username[:-len('-prz-edu-pl')]


    # Konfiguracja wolumenów (bez zmian)
    volumes = {
        f"jupyterhub-user-{safe_username}-work": {"bind": "/home/jovyan/work", "mode": "rw"},
        "jupyterhub-public": {"bind": "/home/jovyan/public", "mode": "ro"},
        "readme_dir": {"bind": "/home/jovyan/-README-", "mode": "ro"}
    }

    if not is_six_digits_username(username):
        volumes[f"jupyterhub-user-{safe_username}-my_public"] = {
            "bind": "/home/jovyan/work/-my_public-",
            "mode": "rw"
        }
    spawner.volumes = volumes

c.Spawner.pre_spawn_hook = setup_user_environment
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"



# Ustawienia trybu testowego (DummyAuthenticator)
c.Authenticator.admin_users = {"admin"}
c.JupyterHub.authenticator_class = "dummy"  # Użycie DummyAuthenticator w trybie testowym

# Konfiguracja Idle Culler (usuwanie bezczynnych serwerów)
c.JupyterHub.load_roles = [
    {
        "name": "jupyterhub-idle-culler-role",
        "scopes": [
            "list:users",
            "read:users:activity",
            "read:servers",
            "delete:servers",
        ],
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