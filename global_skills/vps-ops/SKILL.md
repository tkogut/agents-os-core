---
name: vps-ops
description: Instrukcja i automatyzacja pracy z serwerem VPS, Docker Compose, rebuildami, zmianą branchy i konfiguracją env. Zawiera wzorce API-first monitoringu i obsługi Traefik.
trigger_words: ["vps deploy", "vps setup", "docker-compose rebuild", "deploy production", "setup env vps", "git branch switch vps", "redeploy", "zrób redeploy", "przebuduj kontener"]
---

# VPS Operations & Docker Deploy (v4.3)

## Purpose
Standard pracy, wdrażania i diagnostyki na serwerach VPS z Docker Compose + Traefik.
Wersja 4.3 wprowadza: **API-first monitoring**, wzorce URL Traefik, obsługę slim kontenerów.

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

## 3. Rebuild & Deploy

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

## 7. Wzorce wydajności — lekcje z portfolio-sentinel

### Problem: długotrwałe procesy (signal_engine)

**Antywzorzec** — scraping 240+ tickerów bez cache:
```python
# ZLE: wywołuje HTTP dla każdego tickera przy każdym uruchomieniu
analyze_sentiment()  # może trwać 60+ minut
```

**Wzorzec** — cache TTL + hard timeout:
```python
CACHE_TTL = 6 * 3600  # 6 godzin
cache_age = time.time() - os.path.getmtime(cache_path)
if cache_age < CACHE_TTL:
    # użyj cache
else:
    # odśwież z timeout
    with ThreadPoolExecutor(max_workers=15) as executor:
        # ... max 180 sekund
```

### Problem: batch download danych (yfinance)

```python
# DOBRZE: jeden batch zamiast pętli
data = yf.download(symbols, period="2y", interval="1d", progress=False)
# Przetwarza lokalnie dla każdego tickera — bez dodatkowych requestów
for ticker in symbols:
    prices = data['Close'][ticker].dropna()
```

---

## 8. Usage Rules for Agent

1. **Zawsze czytaj TRAEFIK_HOST z .env** — nie zgaduj IP/domeny.
2. **API-first** — przed SSH sprawdź `/api/status/sync` i `/api/debug/ps`.
3. **Po deployu** — weryfikuj przez API (nowy SHA w `version`), nie przez SSH.
4. **Slim kontenery** — `ps`, `top`, `htop` nie działają. Używaj `/proc` lub API.
5. **Deploy = git pull + docker compose up -d --build + docker system prune -f**.
6. **Watcher pattern** — monitoruj długie procesy co 3 min przez API, nie przez SSH polling.
