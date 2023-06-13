# JupyterHub - Docker

## Uruchomienie
> docker-compose build

> docker-compose run -d

## Konfiguracja
Przed pierwszym uruchomieniem wymagane jest skonfigurowanie środowiska. W tym celu należy edytować plik `.env` a w nim zmienić wartości zmiennych środowiskowych. 

Dodatkowo wymagane jest wgranie certyfikatów TLS do `/app/proxy/certs/` *(korzystając z nazewnictwa plików: cert-host-key.pem oraz cer-host.pem)*.

## Osobne katalogi dla użytkowników
*W trakcie pracy*

W celu rozdzielenia danych użytkowników na nauczycieli oraz studentów, system wykrywa przedrostek `@stud.prz.edu.pl` oraz `@prz.edu.pl`, a następnie dzieli użytkowników na dwie grupy. Odbywa się to w pliku `/app/jupyterhub/config.py`, w funkcji `MyDockerSpawner`.

# TODO

## Projekt
- [x] Przygotowanie pliku docker-compose.yml
- [x] Uporządkowanie struktury projektu
## JupyterHub
- [x] Przygodowanie dla uwierzytelniania CAS
- [x] Przygotowanie pliku juptyerhub_config.py
- [x] Zmiana katalogu z danymi użytkowników
- [ ] Dodanie obsługi kursów
- [ ] Problem z uprawnieniami do katalogów użytkowników [Tu występuje taki sam błąd](https://github.com/jupyterhub/dockerspawner/issues/160)
## Proxy
- [x] Przygotowanie pliku traefik.yml
- [x] Dodanie obsługi HTTPS
- [x] Konfiguracja certyfikatów
## Notebook
- [x] Naprawa braku uprawnień przy tworzeniu nowego notebooka
- [x] Dodanie jądra Julii i R
- [ ] Dodanie obsługi C++
- [ ] Przygotowanie pliku z paczkami pythona


## Struktura repozytorium
```
JupyterHub
├── .env
├── README.md
├── docker-compose.yml
├── app
│   ├── jupyterhub
│   │   ├── Dockerfile
|   |   └── config.py
│   |── jupyterlab
│   |   └── Dockerfile
|   |── proxy
│   |   |── Dockerfile
│   |   |── traefik.yml
│   |   |── tls.yml
│   |   |── certs
│   |   |   ├── localhost-key.pem
│   |   |   └── localhost.pem
├── appdata
│   ├── teachers
│   ├── students
│   └── others
```

# Dokumentacja
## 1. JupyterHub
Wersja: jupyterhub/jupyterhub:3.1.1

*(Znajduje się w /app/jupyterhub/Dockerfile oraz konfiguracja w /app/jupyterhub/config.py)*

[JupyterHub config file](https://github.com/jupyterhub/jupyterhub-deploy-docker)

## 2. Proxy
Wersja: traefik:v2.9

Konfiguracja pliku TLS, musi znajdować się w osobnym pliku!, w tym przypadku jest to tls.yml

*(Znajduje się w /app/proxy/Dockerfile oraz konfiguracja w /app/proxy/traefik.yml)*

[Traefik documentation](https://doc.traefik.io/traefik/)

[Traefik config entry poionts](https://doc.traefik.io/traefik/routing/entrypoints/)

## 3. Notebook
Wersja: jupyter/scipy-notebook:hub-3.1.1

*(Znajduje się w /app/jupyterlab/Dockerfile)*

[Building Docker image for Jupyter Notebook](https://jupyterhub-dockerspawner.readthedocs.io/en/latest/docker-image.html)

[Datascience-notebook](https://hub.docker.com/r/jupyter/datascience-notebook/tags/)

## 4. JHubAuthenticators - CAS Authentication
Wersja: jhubauthenticators==1.0.2

*(Znajduje się w /app/jupyterhub/Dockerfile oraz konfiguracja w /app/jupyterhub/config.py)*

[CAS authenticator](https://github.com/cwaldbieser/jhub_cas_authenticator)

## 5. JupyterHub Idle Culler Service
Wersja 1.2.1

*(Znajduje się w /app/jupyterhub/Dockerfile oraz konfiguracja w /app/jupyterhub/config.py)*

[JupyterHub Idle Culler Service](https://github.com/jupyterhub/jupyterhub-idle-culler)
