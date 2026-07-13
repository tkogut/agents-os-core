---
name: vps-ops
description: Instrukcja i automatyzacja pracy z serwerem VPS, Docker Compose, rebuildami, zmianą branchy i konfiguracją env. Zawiera wzorce API-first monitoringu i obsługi Traefik.
trigger_words: ["vps deploy", "vps setup", "docker-compose rebuild", "deploy production", "setup env vps", "git branch switch vps", "redeploy", "zrób redeploy", "przebuduj kontener"]
---

# VPS Operations & Docker Deploy (v5.0)

## Purpose
Standard pracy, wdrażania i diagnostyki na serwerach VPS z Docker Compose + Traefik.
Wersja 5.0 wprowadza: **wzorzec izolacji wielu instancji tej samej usługi za Traefikiem** (np. wiele instancji n8n dla różnych użytkowników).

---

## 0. PROTOKÓŁ UWIERZYTELNIENIA SSH (CZYTAJ PRZED WSZYSTKIM INNYM)

> **KRYTYCZNE**: Agent CLI działa w izolowanym procesie WSL bez dostępu do `ssh-agent` użytkownika.
> Bez wykonania tego protokołu KAŻDA komenda SSH będzie wisiała, pytając o hasło.
> Wykonaj ten protokół RAZ na początku każdej sesji pracy z VPS.

### Środowisko Hostinger VPS (tkogut)
```
VPS host:    srv1490214.hstgr.cloud
VPS user:    root
Klucz SSH:   ~/.ssh/tkogut_ssh_key  (w WSL)
Źródło klucza: /mnt/c/Users/tkogut/.ssh/id_ed25519/tkogut_ssh_key (na Windows)
```

---

### KROK 0.1 — Sprawdź czy klucz istnieje w WSL

**Gdzie wpisać:** Terminal WSL na lokalnym komputerze (nie VPS!)

```bash
ls -la ~/.ssh/tkogut_ssh_key
```

**Jeśli plik NIE istnieje** → przejdź do kroku 0.2.  
**Jeśli plik istnieje** → przejdź do kroku 0.3.

---

### KROK 0.2 — Skopiuj klucz z Windows do WSL (tylko raz)

**Gdzie wpisać:** Terminal WSL na lokalnym komputerze

```bash
cp /mnt/c/Users/tkogut/.ssh/id_ed25519/tkogut_ssh_key ~/.ssh/tkogut_ssh_key
chmod 600 ~/.ssh/tkogut_ssh_key
```

> ⚠️ Krok `chmod 600` jest OBOWIĄZKOWY. Bez niego SSH odrzuci klucz z błędem
> `WARNING: UNPROTECTED PRIVATE KEY FILE!` i nie nawiąże połączenia.

---

### KROK 0.3 — Uruchom ssh-agent i załaduj klucz

**Gdzie wpisać:** Terminal WSL na lokalnym komputerze (ten sam, w którym pracujesz)

```bash
eval $(ssh-agent -s)
ssh-add ~/.ssh/tkogut_ssh_key
```

**Co zobaczysz na ekranie:**
```
Agent pid 12345
Enter passphrase for /home/tkogut/.ssh/tkogut_ssh_key:
```

Wpisz passphrase (hasło do klucza SSH) gdy zostaniesz poproszony.

**Po wpisaniu poprawnego hasła zobaczysz:**
```
Identity added: /home/tkogut/.ssh/tkogut_ssh_key
```

> ℹ️ Passphrase to hasło ustawione podczas TWORZENIA klucza SSH (np. w panelu Hostinger
> lub przez `ssh-keygen`). To NIE jest hasło do serwera VPS ani do GitHuba.

---

### KROK 0.4 — Pobierz wartość SSH_AUTH_SOCK i przekaż agentowi

**Gdzie wpisać:** Ten sam terminal WSL co w kroku 0.3

```bash
echo "SSH_AUTH_SOCK=$SSH_AUTH_SOCK"
```

**Przykładowy wynik:**
```
SSH_AUTH_SOCK=/tmp/ssh-00B5ZXHusAbx/agent.106006
```

Skopiuj tę wartość i **wklej ją do czatu z agentem**. Agent użyje jej jako prefiksu
do wszystkich komend SSH w tej sesji.

---

### KROK 0.5 — Agent weryfikuje połączenie (wykonuje Agent CLI)

Agent CLI od tej chwili używa SSH_AUTH_SOCK z poprzedniego kroku. Wzorzec każdej komendy SSH:

```bash
SSH_AUTH_SOCK=<wartość_z_kroku_0.4> ssh -o ConnectTimeout=15 -o StrictHostKeyChecking=no root@srv1490214.hstgr.cloud "<komenda_na_VPS>"
```

Test połączenia (wykonuje Agent CLI automatycznie):
```bash
SSH_AUTH_SOCK=/tmp/ssh-XXXX/agent.YYYY ssh -o StrictHostKeyChecking=no root@srv1490214.hstgr.cloud "echo OK && docker --version"
```

**Oczekiwany wynik:**
```
OK
Docker version 24.x.x
```

---

### KROK 0.6 — Autoryzacja GitHub na VPS (tylko przy pierwszym wdrożeniu)

**Gdzie wpisać:** Na VPS (przez SSH lub bezpośrednio w terminalu VPS)

GitHub CLI jest zainstalowany na VPS (`gh --version` → `gh version 2.94.0`).
Aby VPS mógł pobierać kod z prywatnych repozytoriów bez podawania hasła:

```bash
gh auth login
```

Następnie wybierz:
- `GitHub.com`
- `HTTPS`
- `Yes` (Authenticate Git with credentials)
- `Login with a web browser`

Otwórz podany link w przeglądarce, wpisz 8-znakowy kod i zatwierdź.

> ✅ Po autoryzacji `gh` komenda `git clone https://github.com/...` na VPS
> działa bez podawania tokenów ani haseł.

---

### Typowe błędy i rozwiązania

| Błąd | Przyczyna | Rozwiązanie |
|------|-----------|-------------|
| `WARNING: UNPROTECTED PRIVATE KEY FILE!` | Złe uprawnienia klucza (0777) | `chmod 600 ~/.ssh/tkogut_ssh_key` |
| `Enter passphrase for key '...'` | Agent nie załadowany | Wykonaj krok 0.3 |
| `root@srv...'s password:` | Brak klucza w `authorized_keys` na VPS lub brak SSH_AUTH_SOCK | Sprawdź SSH_AUTH_SOCK, wykonaj krok 0.4 |
| `Permission denied (publickey)` | Klucz publiczny nie dodany na VPS | Dodaj klucz przez panel Hostinger |
| `no configuration file provided: not found` | Brak `docker-compose.yml` w katalogu | Sprawdź `git status` i `ls -la` |
| `fatal: Authentication failed for 'https://github.com/...'` | Brak `gh auth login` na VPS | Wykonaj krok 0.6 |
| `Password authentication is not supported` | Próba logowania hasłem do GitHub | Użyj tokenu PAT lub `gh auth login` |
| Komenda wisi bez odpowiedzi | SSH_AUTH_SOCK puste lub wygasłe | Powtórz kroki 0.3 i 0.4 |

---

### Ważne przestrogi

1. **Nie próbuj odczytywać pliku klucza prywatnego** (`id_rsa`, `id_ed25519`). Agent nie potrzebuje
   zawartości klucza — potrzebuje tylko `SSH_AUTH_SOCK`.
2. **SSH_AUTH_SOCK wygasa** po zamknięciu terminala. Przy nowej sesji powtórz kroki 0.3 i 0.4.
3. **Nie montuj `.gitconfig` jako volume read-only** w Dockerze — nadpisuje ustawienie
   `safe.directory` i powoduje błąd `git diff --cached`.
4. **Repozytorium na VPS** zawsze klonuj do właściwej lokalizacji: `/docker/agents-os`
   (nie `/root/agents-os` — brak uprawnień zapisu poza kontekstem sudo).
5. **Sprawdź `git remote -v`** zanim zaczniesz wdrożenie — upewnij się że lokalne repo
   i VPS wskazują na to samo zdalne repozytorium.

---

## 1. Konfiguracja VPS — odczyt z .env

ZAWSZE czytaj dane połączenia z pliku `.env` projektu:

```bash
cat .env | grep -iE "(host|ssh|server|vps|traefik)"
```

Typowe zmienne:
```env
TRAEFIK_HOST=srv1490214.hstgr.cloud        # hostname VPS
HOSTINGER_VPS_ID=1490214                   # ID serwera (opcjonalnie)
```

SSH do VPS:
```bash
ssh -o ConnectTimeout=15 -o StrictHostKeyChecking=no root@srv1490214.hstgr.cloud
```

Wzorzec URL dla usług za Traefik:
```
https://{service-name}.{TRAEFIK_HOST}
# Przykład: https://portfolio-sentinel.srv1490214.hstgr.cloud
```

---

## 2. API-First Monitoring (PRIORYTET nad SSH)

**Zasada**: Zanim sięgniesz po SSH — użyj endpointów API. Szybciej, bez potrzeby klikania.

### Standardowe endpointy diagnostyczne

```bash
# Status synchronizacji (GREEN / ORANGE / RED)
curl -s https://{service}.{TRAEFIK_HOST}/api/status/sync

# Lista procesów (działa w slim kontenerach bez `ps`)
curl -s https://{service}.{TRAEFIK_HOST}/api/debug/ps

# Logi aplikacji
curl -s https://{service}.{TRAEFIK_HOST}/api/debug/logs?lines=50
```

### Implementacja /api/debug/ps (dla slim kontenerów)

Kontenery oparte na `python:slim` **nie mają komendy `ps`**. Implementacja przez `/proc`:

```python
@app.route("/api/debug/ps")
def debug_ps():
    output = []
    for pid in os.listdir("/proc"):
        if pid.isdigit():
            try:
                with open(f"/proc/{pid}/cmdline", "r") as f:
                    cmd = f.read().replace("\x00", " ").strip()
                if cmd:
                    output.append(f"PID {pid:<6}: {cmd[:80]}")
            except:
                pass
    return "\n".join(sorted(output))
```

### Monitoring procesu — wzorzec watchera

```python
# Sprawdź co 3 minuty czy proces zakończył pracę
curl -s https://{service}.{TRAEFIK_HOST}/api/debug/ps | grep signal_engine
# Brak wyniku = proces zakończony
```

---

## 3. Adaptive Process Watcher (OBOWIĄZKOWY PROTOKÓŁ)

Gdy agent monitoruje długotrwały proces (signal_engine, data_loader, itp.):

### Krok 1 — Zapytaj użytkownika o interwał

**ZAWSZE** przed uruchomieniem watchera zapytaj:
> „Co ile mam sprawdzać czy proces się zakończył? (domyślnie: 1 minuta)"

Czekaj **max 30 sekund** na odpowiedź. Jeśli brak — ustaw 1 minutę.

Przykładowe odpowiedzi użytkownika:
- `"co 3 minuty"` → `interval = 3 min`
- `"co 5 min"` → `interval = 5 min`
- `"sprawdzaj często"` → `interval = 30 sekund`
- brak odpowiedzi → `interval = 1 min` (default)

### Krok 2 — Dynamiczna adaptacja interwału

Po każdej iteracji agent **aktualizuje interwał** na podstawie czasu życia procesu:

```
elapsed_time → next_interval

0  – 5 min   → max(user_default, 1 min)    # wczesna faza — częste sprawdzanie
5  – 15 min  → max(user_default, 3 min)    # środkowa faza — umiarkowane
15 – 30 min  → max(user_default, 5 min)    # długa faza — rzadsze sprawdzanie
30+  min     → max(user_default, 10 min)   # bardzo długa — oszczędność zasobów
```

**Reguła**: nowy interwał = `max(user_default, adaptive_interval)`.
Nigdy nie sprawdzaj **rzadziej** niż pozwolił użytkownik, ale możesz **częściej**.

### Krok 3 — Raportowanie

Przy każdej iteracji informuj użytkownika:
```
🟠 Iteracja 3 | Czas: 9 min | Następne sprawdzenie za: 3 min | PID 2400 żyje
```

Po zakończeniu procesu:
```
✅ PID 2400 zakończony po ~12 min | Przystępuję do implementacji...
```

### Implementacja w schedule tool

```python
# Iteracja 1 (elapsed=0):      interval = 1 min  (default)
# Iteracja 3 (elapsed=6 min):  interval = 3 min  (adaptacja)
# Iteracja 8 (elapsed=20 min): interval = 5 min  (adaptacja)
# Iteracja 15 (elapsed=40min): interval = 10 min (adaptacja)
```

Użyj `schedule` tool z dynamicznie obliczonym `DurationSeconds`:
- 1 min → `DurationSeconds=60`
- 3 min → `DurationSeconds=180`
- 5 min → `DurationSeconds=300`
- 10 min → `DurationSeconds=600`

---

## 4. Rebuild & Deploy

### Standardowa procedura (przez SSH)

```bash
ssh root@{TRAEFIK_HOST} "
  cd /root/{project-dir} && \
  git pull origin master && \
  docker compose up -d --build && \
  docker system prune -f && \
  docker compose ps
"
```

### Lokalny deploy-helper.sh

```bash
# Użyj skryptu z projektu jeśli istnieje:
bash .agents/skills/vps-ops/scripts/deploy-helper.sh
# lub z niestandardową gałęzią:
bash .agents/skills/vps-ops/scripts/deploy-helper.sh -b production
```

### Weryfikacja po deployu

```bash
# 1. Sprawdź status API (powinno zwrócić nową wersję)
curl -s https://{service}.{TRAEFIK_HOST}/api/status/sync
# Oczekiwany output: {"status":"ORANGE","version":"master@<new_sha>"}

# 2. Po zakończeniu sync — GREEN
# {"status":"GREEN","version":"master@<new_sha>"}
```

---

## 4. Zmiana branchy (Git branch swap na VPS)

```bash
ssh root@{TRAEFIK_HOST} "
  cd /root/{project-dir} && \
  git fetch --all && \
  git stash && \
  git checkout {branch} && \
  git pull origin {branch} && \
  git stash pop || true && \
  docker compose up -d --build
"
```

---

## 5. Setup .env

```bash
# .env NIGDY nie jest w repo — twórz ręcznie na VPS
cp .env.example .env
nano .env

# Generowanie bezpiecznych kluczy
openssl rand -hex 32
```

---

## 6. Diagnostyka błędów

### Sprawdzenie logów aplikacji w kontenerze

```bash
# Przez API (preferowane)
curl -s https://{service}.{TRAEFIK_HOST}/api/debug/logs

# Przez SSH — logi Docker
ssh root@{TRAEFIK_HOST} "docker compose logs --tail=100 api"

# Logi błędów z pliku w wolumenie
ssh root@{TRAEFIK_HOST} "cat /root/{project}/.tmp/api_errors.log | tail -30"
```

### Typowe problemy

| Problem | Przyczyna | Rozwiązanie |
|---------|-----------|-------------|
| API zwraca stary SHA wersji | Kontener nie przebudowany | `docker compose up -d --build` |
| `/api/debug/ps` nie działa | Brak endpointu w API | Dodaj endpoint czytający `/proc` |
| `ps` nie działa w kontenerze | Slim image bez procps | Użyj `/proc` lub API endpoint |
| Proces wisi godzinami | Brak timeout (np. sentiment scraper) | Dodaj hard timeout + cache TTL |
| 404 na tickerach US | Błędny suffix `.WA` na US tickerach | Sprawdź `get_market_map()` |

---

## 7. Wzorce wydajności — Production Patterns

### P1: Długotrwałe zadania — Cache TTL + Hard Timeout

Każde zadanie scrapujące/pobierające dane dla N>50 elementów MUSI mieć:

```python
# ANTYWZORZEC: wywołanie HTTP dla każdego elementu przy każdym uruchomieniu
fetch_all_items()  # 100 elementów × 1-3s = 100-300s blokady

# WZORZEC: cache TTL + hard timeout + więcej workerów
CACHE_TTL = 6 * 3600  # 6 godzin — nie odświeżaj częściej
cache_age = time.time() - os.path.getmtime(cache_path) if os.path.exists(cache_path) else float('inf')
if cache_age < CACHE_TTL:
    load_from_cache()  # szybko
else:
    HARD_TIMEOUT = 180  # 3 minuty max
    with ThreadPoolExecutor(max_workers=15) as executor:
        for future in as_completed(futures, timeout=HARD_TIMEOUT):
            try:
                result = future.result(timeout=12)
            except Exception:
                pass  # skip failed items
```

### P2: Batch download zamiast pętli requestów

```python
# ANTYWZORZEC: N requestów = N × opóźnienie sieci
for symbol in symbols:
    data = fetch_single(symbol)  # wolne, ryzyko rate-limit

# WZORZEC: jeden batch request
data = fetch_batch(symbols)  # jeden request, przetwarzaj lokalnie
for symbol in symbols:
    result = process_local(data[symbol])
```

### P3: Jitter i backoff przy zewnętrznych API

```python
# Zbyt duży jitter blokuje cały pipeline
time.sleep(random.uniform(1.0, 3.0))  # ZLE przy 100+ elementach

# Minimalny jitter wystarczy przy wielu workerach
time.sleep(random.uniform(0.05, 0.5))  # DOBRZE

# Przy niepowodzeniach: exponential backoff
for attempt in range(3):
    try:
        result = call_api()
        break
    except Exception:
        time.sleep(0.5 * (2 ** attempt))  # 0.5s, 1s, 2s
```

---

## 8. API Design dla Agentów AI (Best Practices)

Jeśli budujesz aplikację zarządzaną przez agenta AI, zaprojektuj API tak:

### Obowiązkowe endpointy

```
GET /api/status          → {"status": "GREEN|ORANGE|RED", "version": "master@abc123"}
GET /api/debug/ps        → lista procesów (czyta /proc — działa w slim containers)
GET /api/debug/logs      → ostatnie N linii logów
GET /api/version         → {"sha": "abc123", "deployed_at": "2026-06-06T..."}
```

### Long-running jobs pattern

```python
# Agent wywołuje: POST /api/jobs/sync
# Natychmiastowa odpowiedź:
{"job_id": "sync-001", "status": "STARTED"}

# Agent polluje: GET /api/jobs/sync-001/status
{"job_id": "sync-001", "status": "RUNNING", "progress": "45/240 tickers"}
{"job_id": "sync-001", "status": "DONE", "elapsed_s": 312}
```

### Strukturalne błędy (nie HTML 500)

```python
# Agent nie umie parsować HTML stack trace
# ZLE: return 500 Internal Server Error (HTML)
# DOBRZE:
return {"error": "timeout", "details": "yfinance download exceeded 30s", "ticker": "AAPL"}, 500
```

---

## 9. Docker Volumes — co przeżywa rebuild

Agent MUSI wiedzieć co resetuje się po `docker compose up --build`:

| Zasób | Przeżywa rebuild? | Dlaczego |
|-------|------------------|----------|
| Kod aplikacji | ❌ Zastąpiony | Nowy image z git pull |
| `.env` (volume mount) | ✅ TAK | Montowany z hosta |
| `database.db` (volume mount) | ✅ TAK | Montowany z hosta |
| `.tmp/` cache (volume mount) | ✅ TAK | Montowany z hosta |
| Zmienne środowiskowe | ✅ TAK | Z `docker-compose.yml` |
| Dane w kontenerze (nie volume) | ❌ Utracone | Ephemeral layer |

**Reguła**: wszystko co ma przeżyć rebuild musi być w `volumes:` w `docker-compose.yml`.

---

## 10. CI/CD bez SSH (GitHub Actions)

Najlepszy pattern dla agenta — push kodu → automatyczny deploy:

```yaml
# .github/workflows/deploy.yml
on:
  push:
    branches: [master]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to VPS
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.VPS_HOST }}
          username: root
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /root/{project}
            git pull origin master
            docker compose up -d --build
            docker system prune -f
```

Agent push → CI/CD deploy → Agent weryfikuje przez `/api/version` czy nowy SHA wdrożony.
**Zero SSH po stronie agenta.**

---

## 11. Usage Rules for Agent

1. **Zawsze czytaj TRAEFIK_HOST z .env** — nie zgaduj IP/domeny.
2. **API-first** — przed SSH sprawdź `/api/status` i `/api/debug/ps`.
3. **Po deployu** — weryfikuj przez `/api/version` (nowy SHA), nie przez SSH.
4. **Slim kontenery** — `ps`, `top`, `htop` nie działają. Używaj `/proc` lub API.
5. **Deploy = git pull + docker compose up -d --build + docker system prune -f**.
6. **Adaptive Watcher** — zapytaj o interwał, domyślnie 1 min, adaptuj dynamicznie.
7. **Cache przed requestem** — sprawdź wiek cache przed wywołaniem kosztownego API.
8. **Volumes check** — przed rebuild sprawdź co jest zamontowane jako volume.
9. **Strukturalne logi** — aplikacja musi logować do pliku w volume, nie tylko stdout.
10. **Nie trzymaj stanu w kontekście** — każdą sesję zacznij od `curl /api/version`.
11. **Multi-instance isolation** — jedna instancja = jeden kontener + jeden wolumen + jedna subdomena. Nigdy nie współdziel wolumenu między instancjami tej samej usługi.

---

## 12. Traefik Multi-Instance Isolation Pattern

Wzorzec dla uruchomienia wielu izolowanych instancji tej samej usługi (np. n8n dla różnych użytkowników).

> **Zasada**: Każda instancja = osobny katalog `/docker/<name>/`, osobny wolumen, osobna subdomena.

### Wymagania
- Sieć Docker `traefik-proxy` musi istnieć: `docker network create traefik-proxy`
- Traefik musi być skonfigurowany z resolverem `letsencrypt` (standardowo na VPS Hostinger)

### Wzorzec `docker-compose.yml`

```yaml
services:
  app:
    image: <image>
    restart: unless-stopped
    volumes:
      - app_data_<name>:/data  # osobny wolumen per instancja
    networks:
      - traefik-proxy
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.<name>.rule=Host(`<name>.srv1490214.hstgr.cloud`)"
      - "traefik.http.routers.<name>.entrypoints=websecure"
      - "traefik.http.routers.<name>.tls.certresolver=letsencrypt"
      - "traefik.http.services.<name>.loadbalancer.server.port=<port>"

networks:
  traefik-proxy:
    external: true  # KLUCZOWE: nie twórz nowej sieci, używaj istniejącej

volumes:
  app_data_<name>:  # unikalny sufiks per instancja
```

### Procedura wdrożenia nowej instancji

```bash
# 1. Utwórz katalog
mkdir -p /docker/<name>

# 2. Wgraj docker-compose.yml i .env
# ... (scp lub heredoc)

# 3. Uruchom
cd /docker/<name> && docker compose up -d

# 4. Weryfikacja
docker ps | grep <name>  # status: Up
```

### Rzeczywiste instancje na srv1490214.hstgr.cloud

| Katalog | Kontener | URL | Użytkownik |
|---------|----------|-----|------------|
| `/docker/n8n-g7tq` | `n8n-g7tq-n8n-1` | `https://n8n-g7tq.srv1490214.hstgr.cloud` | tkogut |
| `/docker/n8n-pkogut` | `n8n-pkogut-n8n-1` | `https://n8n-pkogut.srv1490214.hstgr.cloud` | pkogut |

> ℹ️ n8n Free tier: 1 użytkownik per instancja. Nowy użytkownik = nowa izolowana instancja.

---

## 13. Automated VPS Operations with `vps_helper.py` (Recommended)

W katalogu `global_skills/vps-ops/scripts/` (lub w folderze `.agents/skills/vps-ops/scripts/` lokalnego projektu) znajduje się skrypt pomocniczy automatyzujący całą diagnostykę i wdrażanie aplikacji na VPS.

### 13.1 Sprawdzenie statusu serwera i kontenerów
```bash
python3 scripts/vps_helper.py status
```
*(Automatycznie wykrywa gniazdo SSH agenta, łączy się z VPS, pobiera listę kontenerów oraz informacje o wolnej pamięci RAM i dysku).*

### 13.2 Aktualizacja i wdrożenie projektu (Deploy)
```bash
python3 scripts/vps_helper.py deploy --dir /docker/n8n-g7tq --branch master
```
*(Zabezpiecza lokalne modyfikacje na VPS przez git stash, pobiera najnowsze pliki z określonej gałęzi, buduje i restartuje kontenery docker compose w tle).*

### 13.3 Odczyt logów kontenera lub projektu
* Dla pojedynczego kontenera:
  ```bash
  python3 scripts/vps_helper.py logs --container n8n-g7tq-n8n-1 --lines 100
  ```
* Dla całego stacku docker compose w folderze:
  ```bash
  python3 scripts/vps_helper.py logs --dir /docker/n8n-g7tq --lines 50
  ```
* Śledzenie logów na żywo (wymaga interaktywnej konsoli):
  ```bash
  python3 scripts/vps_helper.py logs --container n8n-g7tq-n8n-1 -f
  ```

### 13.4 Bezpieczny odczyt i modyfikacja pliku `.env` na VPS
* Podgląd całego pliku `.env`:
  ```bash
  python3 scripts/vps_helper.py env get --dir /docker/n8n-g7tq
  ```
* Pobranie wartości konkretnego klucza:
  ```bash
  python3 scripts/vps_helper.py env get --dir /docker/n8n-g7tq --key TIMEZONE
  ```
* Zmiana wartości (lub dodanie nowej zmiennej):
  ```bash
  python3 scripts/vps_helper.py env set --dir /docker/n8n-g7tq --key TIMEZONE --value Europe/Warsaw
  ```
  *(Automatycznie koduje treść za pomocą base64 w celu uniknięcia błędów parsowania znaków specjalnych w konsoli).*

