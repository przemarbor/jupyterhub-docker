# JupyterHub - Docker

## Pierwsze uruchomienie

### Konfiguracja wstępna
Przed pierwszym uruchomieniem wymagane jest skonfigurowanie środowiska. W tym celu należy:

- edytować plik `.env`. W szczególności zmienić wartość zmiennej środowiskowej HOST (`HOST=localhost` `->` `HOST=jupyterhub.xxx.edu.pl`)
 
- Edycja adresu email administratora dla którego jest generowany certyfikat w pliku `/app/proxy/traefik.yml` (`certificatesResolvers -> tlsresolver -> acme: -> email:`)

- Ustalenie administratora odbywa się w pliku `/app/jupyterhub/jupyterhub_config.py` w zmiennej `c.Authenticator.admin_users`. W celu ustawienia osoby z organizacji jako administratora należy dodać jej adres email do tej zmiennej (np. `123456@xxx.edu.pl`).

- ~~dodatkowo wymagane jest wgranie certyfikatów TLS do `/app/proxy/certs/` *(korzystając z nazewnictwa plików: cert-host-key.pem oraz cer-host.pem)*.~~

  Traefik sam generuje certyfikaty TLS, więc nie jest już wymagane ich wgranie.


### Uruchomienie

> docker-compose build

> docker-compose run -d

MBnote: nie udalo sie uruchomic `docker-compose run -d`. Zamiast
tego lepiej sprobowac:

> docker-compose up -d

tego lepiej sprobowac (roznica miedzy `docker-compose up` a `docker-compose run`).

Usługi szukac pod `https`, np. [https://jupyterhub.xxx.edu.pl](https://jupyterhub.xxx.edu.pl).

Dostęp do JupyterHuba: `https://{nazwa_hosta}` (domyślnie port 80 HTTP jest wyłączony, przez co wymaga użycia HTTPS)

## Osobne katalogi dla użytkowników
*W trakcie pracy*

W celu rozdzielenia danych użytkowników na nauczycieli oraz studentów, system wykrywa przedrostek `@stud.xxx.edu.pl` oraz `@xxx.edu.pl`, a następnie dzieli użytkowników na dwie grupy. Odbywa się to w pliku `/app/jupyterhub/config.py`, w funkcji `MyDockerSpawner`.

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
- [x] Automatyczne generowanie certyfikatów
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
|   |   └── jupyterhub_config.py
│   |── jupyterlab
│   |   └── Dockerfile
|   |── proxy
│   |   |── Dockerfile
│   |   |── traefik.yml

```

# Dokumentacja
## 1. JupyterHub
Wersja: jupyterhub/jupyterhub:3.1.1

*(Znajduje się w /app/jupyterhub/Dockerfile oraz konfiguracja w /app/jupyterhub/jupyterhub_config.py)*

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

*(Znajduje się w /app/jupyterhub/Dockerfile oraz konfiguracja w /app/jupyterhub/jupyterhub_config.py)*

[CAS authenticator](https://github.com/cwaldbieser/jhub_cas_authenticator)

## 5. JupyterHub Idle Culler Service
Wersja 1.2.1

*(Znajduje się w /app/jupyterhub/Dockerfile oraz konfiguracja w /app/jupyterhub/jupyterhub_config.py)*

[JupyterHub Idle Culler Service](https://github.com/jupyterhub/jupyterhub-idle-culler)

## 6. Docker-compose with let's encrypt: TLS Challenge
Konfiguracja automatycznego generowania certyfikatów TLS, oparta na wykorzystaniu Let's Encrypt.

[Docker-compose with let's encrypt: TLS Challenge](https://doc.traefik.io/traefik/user-guides/docker-compose/acme-tls/)
