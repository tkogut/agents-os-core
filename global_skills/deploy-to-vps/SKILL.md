---
name: deploy-to-vps
description: Standard workspace dla automatycznego wdrożenia projektu na VPS przez GitHub Actions. Zawiera szablon .github/workflows/deploy.yml, skrypt setup-deploy-secrets.sh (klucz SSH + sekret w repo) i instrukcję krok po kroku. Używaj, gdy projekt ma Dockerfile + docker-compose.yml i ma wdrażać się automatycznie.
trigger_words: ["deploy to vps", "github actions deploy", "automatyczny deploy", "workflow deploy", "vps ssh key", "setup deploy secrets", "skonfiguruj deploy"]
---

# 🚀 Deploy to VPS — GitHub Actions (v1.0)

## Cel

Jeden, powtarzalny standard dodawania **automatycznego wdrożenia na wspólny VPS**
(`srv1490214.hstgr.cloud`) do każdego projektu, który ma `Dockerfile` +
`docker-compose.yml`. Wzorzec pochodzi z `linkedin-tracker/.github/workflows/deploy.yml`
i został utwardzony w `osint-lead-tracker` (PR #1).

## Konwencja (dla każdego projektu)

Workflow `.github/workflows/deploy.yml`:

1. trigger: `push` do gałęzi domyślnej (`main`) + `workflow_dispatch`;
2. `concurrency` (jeden deploy na raz) i `permissions: contents: read`;
3. `actions/checkout` → usunięcie `.git`/`.github` → `appleboy/scp-action` kopiuje
   drzewo na VPS do `DEPLOY_PATH`;
4. `appleboy/ssh-action` uruchamia `docker compose up -d --build`, ustawia
   uprawnienia bind-mountowanego katalogu danych, czeka na `HEALTHCHECK`
   kontenera (max 30 × 5 s), potem `docker compose ps` i `docker system prune -f`;
5. **uprawnienia wolumenu danych** — bind mount (`./data:/app/data`) nadpisuje
   właściciela `/app/data` z obrazu, więc katalog utworzony na hoście przez
   roota nie jest zapisywalny dla nieuprzywilejowanego użytkownika kontenera
   (Dockerfile `USER`) i SQLite nie otworzy bazy. Dlatego po `mkdir -p data`:
   `chown -R <UID>:<UID> data` oraz `chmod -R 777 data` (UID kontenera — np. 1001);
6. `.env` **nigdy** nie jest wysyłany (jest w `.gitignore`) — plik na serwerze
   pozostaje nietknięty. Gdy go brak, skrypt odtwarza zmienne z działającego
   kontenera, a w ostateczności kopiuje `.env.example` z ostrzeżeniem;
7. `set -eu` (nie `pipefail` — POSIX `sh`/dash go nie zna), brak zależności od
   `curl` na hoście (stan zdrowia czytany z `docker inspect`).

### Sekrety i zmienne repozytorium

| Sekret | Wymagany | Opis |
|--------|----------|------|
| `VPS_SSH_KEY` | ✅ | Klucz **prywatny**, autoryzowany dla `VPS_USER` na VPS. |
| `VPS_SSH_PASSPHRASE` | ⬜ | Hasło klucza — tylko gdy klucz jest nim zabezpieczony. |

| Zmienna | Domyślnie | Opis |
|---------|-----------|------|
| `VPS_HOST` | `srv1490214.hstgr.cloud` | Host VPS. |
| `VPS_USER` | `root` | Użytkownik SSH. |
| `VPS_PORT` | `22` | Port SSH. |
| `DEPLOY_PATH` | `/docker/<projekt>` | Katalog docelowy na VPS. |

## Jak dodać deploy do projektu

1. Skopiuj `assets/deploy.yml` → `.github/workflows/deploy.yml` i podmień placeholdery:
   `__PROJECT__` (nazwa repo), `__CONTAINER__` (`container_name` z `docker-compose.yml`),
   `__DEFAULT_DEPLOY_PATH__` (domyślny katalog, np. `/docker/<projekt>`),
   `__DATA_UID__` (UID:GID użytkownika kontenera z `USER` w `Dockerfile`, np. `1001`;
   gdy nie wiesz, zostaw `1001` + `chmod 777` i tak rozwiązuje problem).
2. Ustaw sekrety (najlepiej skryptem — patrz niżej):
   `bash .agents/skills/deploy-to-vps/scripts/setup-deploy-secrets.sh <owner>/<repo>`
   (opcje: `--host`, `--port`, `--user`, `--key`, `--deploy-path`, `--passphrase`, `--yes`;
   `--help` wypisuje pełną listę).
3. Sprawdź, czy `DEPLOY_PATH` wskazuje katalog, z którego **aktualnie działa** stack
   (kontener ma stałą nazwę — deploy z innego katalogu odtworzy kontener i może
   podłączyć pusty wolumen `./data`).
4. Commit + PR (workflow nie uruchamia się na PR — tylko na `push` do `main`).
5. Po merge uruchom raz z **Actions → Deploy to VPS → Run workflow**
   (`gh workflow run deploy.yml --repo <owner>/<repo>`).

## Setup sekretów (poprawne komendy)

Nazwa pliku klucza musiała być **identyczna** w `ssh-keygen`, `ssh-copy-id`
i `gh secret set` — to najczęstszy błąd. Wersja kanoniczna:

```bash
PROJECT=osint-lead-tracker
HOST=srv1490214.hstgr.cloud

# 1. Dedykowany klucz CI bez passphrase
ssh-keygen -t ed25519 -f ~/.ssh/${PROJECT}_deploy -N "" -C "github-${PROJECT}"

# 2. Klucz publiczny na VPS
ssh-copy-id -i ~/.ssh/${PROJECT}_deploy.pub root@${HOST}

# 3. Weryfikacja PRZED ustawieniem sekretu
ssh -i ~/.ssh/${PROJECT}_deploy -o IdentitiesOnly=yes root@${HOST} "echo OK && docker --version"

# 4. Sekret = klucz PRYWATNY
gh secret set VPS_SSH_KEY --repo <owner>/${PROJECT} < ~/.ssh/${PROJECT}_deploy
gh secret list --repo <owner>/${PROJECT}

# 5. Opcjonalne zmienne repo
gh variable set VPS_HOST    --repo <owner>/${PROJECT} --body "${HOST}"
gh variable set DEPLOY_PATH --repo <owner>/${PROJECT} --body "/docker/${PROJECT}"
```

Gdy używasz istniejącego klucza z passphrase: dodatkowo
`gh secret set VPS_SSH_PASSPHRASE --repo <owner>/${PROJECT}`.
Zalecany jest jednak **dedykowany klucz per projekt bez hasła** (łatwiejsza rotacja
i odwołanie). Skrypt `scripts/setup-deploy-secrets.sh` wykonuje cały ten przepływ
interaktywnie i nigdy nie wypisuje zawartości klucza.

## Dystrybucja — jak zrobić, żeby „każdy projekt" to miał

- **Nie edytuj `om-setup-agent-pipeline` lokalnie.** To skill z upstreamowej
  kolekcji (`open-mercato/skills`), instalowany przez `npx skills add` i nadpisywany
  przy upgrade. Nie umieszczaj w nim hostów/nazw (`tkogut`, `srv1490214`) ani
  konwencji projektowych.
- **`MEMORY.md` to nie nośnik konwencji** — jest per-projekt i union-merge'owany;
  nowy projekt go nie odziedziczy. Może tylko wskazywać na ten skill.
- **Kanoniczne źródło:** skill `deploy-to-vps` w warstwie AGENTS-OS. Aby stał się
  naprawdę globalny, skopiuj katalog `deploy-to-vps/` do repozytorium
  `agents-os-core` (katalog `vault/`) i dopisz go do `INSTALL.sh` / bootstrapu —
  wtedy `os-init` instaluje go w każdym nowym projekcie.
- **Hook automatyczny:** repo-local override
  `.ai/skills/om-setup-agent-pipeline/SKILL.md` (mechanizm „Per-skill local
  overrides") dodaje do setupu krok „zaproponuj `deploy.yml`". To nie nadpisuje
  upstreamu i działa per projekt.

## Guardrails

- Nie loguj i nie wklejaj klucza prywatnego ani `.env` — `gh secret set` czyta z pliku.
- Skrypt pyta o potwierdzenie przed `ssh-copy-id` i przed ustawieniem sekretu.
- Nie usuwaj `.env` na serwerze; workflow ma go zachować.
- Deploy triggeruje się tylko na `push` do `main`; nie używaj do tego PR-ów.
