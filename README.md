# JupyterHub - Docker

## Wprowadzenie
Niniejszy projekt implementuje środowisko JupyterHub z wykorzystaniem kontenerów Docker, serwera Traefik jako reverse-proxy oraz różnych mechanizmów uwierzytelniania i zarządzania użytkownikami. System jest zdefiniowany w plikach `docker-compose.yml`, `Dockerfile`, `jupyterhub_config.py` oraz `jupyterhub_config_test.py`.

## Konfiguracja i uruchomienie


### Konfiguracja wstępna
Przed pierwszym uruchomieniem wymagane jest skonfigurowanie środowiska, głównie poprzez edycję pliku `.env`.

- **Adres hosta**: Zmień wartość zmiennej środowiskowej `HOST` w pliku `.env` na adres, pod którym JupyterHub będzie dostępny (np. `HOST=jupyterhub.prz.edu.pl`).
  
- **Adres e-mail**: Edytuj adres e-mail administratora w pliku `traefik.yml`. Jest on używany do generowania certyfikatu TLS przez Let's Encrypt.
  
- **Ustalenie administratora**: W pliku `jupyterhub_config.py` dodaj adres e-mail administratora do zmiennej `c.Authenticator.admin_users`.

- ~~dodatkowo wymagane jest wgranie certyfikatów TLS do `/app/proxy/certs/` *(korzystając z nazewnictwa plików: cert-host-key.pem oraz cer-host.pem)*.~~

**Uwaga**: Wgrywanie certyfikatów TLS do `/app/proxy/certs/` nie jest już wymagane, ponieważ Traefik automatycznie generuje certyfikaty za pomocą Let's Encrypt.



### Uruchomienie
Aby uruchomić projekt, skorzystaj z odpowiednich plików docker-compose.yml w zależności od środowiska, którego potrzebujesz.

#### Środowisko produkcyjne
Aby uruchomić serwer produkcyjny, użyj polecenia:

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```
Usługi są dostępne pod adresem https://{HOST} (np. https://jupyterhub.prz.edu.pl).

#### Środowisko testowe
Aby uruchomić serwer testowy (niezależnie od produkcyjnego), użyj polecenia:

```bash
docker-compose -f docker-compose.test.yml up -d --build
```

Wersja testowa dostępna jest na porcie 8443 pod adresem https://{HOST}:8443/test/.


Domyślnie port 80 (HTTP) jest wyłączony, a ruch jest przekierowywany na port 443 (HTTPS).


## Główne funkcjonalności

### 1. Zarządzanie kontenerami użytkowników
* **Dockerspawner**: Tworzenie pojedynczych instancji Jupyter Notebook dla każdego użytkownika.
* **Limity zasobów**: Limity pamięci (`MEM_LIMIT`) i procesora (`CPU_LIMIT`) są konfigurowane dynamicznie.
* **Zarządzanie wolumenami**:
    * Wolumen prywatny dla każdego użytkownika.
    * Wolumen publiczny dla współdzielonych zasobów.

### 2. Uwierzytelnianie
* **CAS Authenticator**: Integracja z systemem uwierzytelniania CAS.
* **Dummy Authenticator**: Tryb testowy dla rozwoju lokalnego.

### 3. Idle Culler
Automatyczne zamykanie nieaktywnych sesji po określonym czasie.

### 4. Reverse Proxy (Traefik)
* Automatyczne zarządzanie certyfikatami SSL.
* Konfiguracja punktów końcowych.

---

## Dokładna specyfikacja dostępu do wolumenów

### 1. Wolumen prywatny (`/home/jovyan/work`)
* **Przeznaczenie**: 
  * Przestrzeń robocza użytkownika
  * Dane prywatne i konfiguracje
  * Ścieżka na hoście: `/var/lib/docker/volumes/jupyterhub-user-<username>-work/_data`

### Wolumen publiczny (`/home/jovyan/public`)
* **Dostęp dla wszystkich użytkowników**:
    * Tylko do odczytu (read-only).
    * Brak możliwości zapisu.
    * Ścieżka na hoście: `/var/lib/docker/volumes/jupyterhub-public/_data`.

### Wolumen `my_public` (specjalny dla wykładowców)
* **Mechanizm działania**:
    * Automatyczne kopiowanie plików z `my_public` do publicznego folderu na hoście.
    * Implementowane przez skrypt monitorujący zmiany za pomocą `inotifywait`.
* **Dostęp**:
    * Tylko wykładowcy (użytkownicy bez 6-cyfrowego ID) mają dostęp do wolumenu (odczyt-zapis).
    * Studenci nie mają do niego dostępu.

### Wolumen informacyjny (`/home/jovyan/-README-`)
* **Dostęp dla wszystkich użytkowników**:
    * Tylko do odczytu (read-only).
    * Brak możliwości zapisu.
    * Ścieżka na hoście: `/var/lib/docker/volumes/readme_dir/_data`.

### Rzeczywiste uprawnienia:
| Wolumen | Studenci (6-cyfrowe ID) | Wykładowcy (inne ID) |
| :--- | :---: | :---: |
| `work` | Odczyt-Zapis | Odczyt-Zapis |
| `public` | Tylko do odczytu | Tylko do odczytu |
| `my_public` | Brak dostępu | Odczyt-Zapis |
| `-README-` | Tylko do odczytu | Tylko do odczytu |

---

## Obejście problemów z folderami publicznymi
System wykorzystuje mechanizm kopiowania z `my_public` do publicznego folderu na hoście, ponieważ:
1.  Docker Volume ma ograniczenia w zarządzaniu uprawnieniami.
2.  Bezpośredni zapis do publicznego wolumenu powodował problemy z synchronizacją.
3.  Rozwiązanie gwarantuje, że tylko zatwierdzone pliki wykładowców trafiają do przestrzeni publicznej.

---

# Status projektu

### Projekt
- [x] Przygotowanie pliku `docker-compose.yml`
- [x] Uporządkowanie struktury projektu
- [x] Rozdzielenie konfiguracji na wersje deweloperską i produkcyjną
- [x] Konfiguracja zmiennych środowiskowych

### JupyterHub
- [x] Rozwiązanie problemów z uprawnieniami
- [x] Przygotowanie dla uwierzytelniania CAS
- [ ] Implementacja systemu kursów

### Notebook
- [x] Naprawa braku uprawnień przy tworzeniu nowego notebooka
- [x] Dodanie jądra Julii i R
- [x] Dodanie obsługi C++
- [x] Przygotowanie pliku z paczkami pythona
- [ ] Dodanie jądra Maximy

### Proxy
- [x] Przygotowanie pliku `traefik.yml`
- [x] Dodanie obsługi HTTPS
- [x] Konfiguracja certyfikatów
- [x] Automatyczne generowanie certyfikatów

## Uwagi
Obecna wersja zawiera wszystkie główne funkcjonalności opisane w dokumentacji. Rozwijamy obecnie:
* System zarządzania kursami
* Dodatkowe języki programowania
* Lepsze monitorowanie zasobów

## Struktura repozytorium

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
