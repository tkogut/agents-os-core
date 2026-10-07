#!/usr/bin/env bash
# ==============================================================================
# setup-deploy-secrets.sh
# Konfiguracja klucza SSH i sekretu VPS_SSH_KEY dla GitHub Actions
# (skill: deploy-to-vps)
#
# Użycie:
#   bash setup-deploy-secrets.sh <owner>/<repo> [opcje]
#
# Opcje:
#   --host HOST          host VPS            (default: srv1490214.hstgr.cloud)
#   --port PORT          port SSH            (default: 22)
#   --user USER          użytkownik SSH      (default: root)
#   --key PATH           ścieżka klucza      (default: ~/.ssh/<repo>_deploy)
#   --deploy-path PATH   DEPLOY_PATH na VPS  (default: /opt/<repo>)
#   --passphrase         klucz z hasłem (bez tego generowany jest bez hasła)
#   --yes                nie pytaj o potwierdzenie (tryb nieinteraktywny)
#   -h|--help            pomoc
#
# Skrypt NIGDY nie wypisuje zawartości klucza prywatnego.
# ==============================================================================
set -euo pipefail

HOST="srv1490214.hstgr.cloud"
PORT="22"
VPS_USER="root"
KEY_PATH=""
DEPLOY_PATH=""
USE_PASSPHRASE=0
ASSUME_YES=0
REPO=""

usage() {
  sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'
  exit "${1:-0}"
}

need_val() {
  [ "$#" -ge 2 ] || { echo "BŁĄD: opcja $1 wymaga wartości." >&2; usage 1; }
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --host)        need_val "$@"; HOST="$2"; shift ;;
    --port)        need_val "$@"; PORT="$2"; shift ;;
    --user)        need_val "$@"; VPS_USER="$2"; shift ;;
    --key)         need_val "$@"; KEY_PATH="$2"; shift ;;
    --deploy-path) need_val "$@"; DEPLOY_PATH="$2"; shift ;;
    --passphrase)  USE_PASSPHRASE=1 ;;
    --yes|-y)      ASSUME_YES=1 ;;
    -h|--help)     usage 0 ;;
    -*)            echo "Nieznana opcja: $1" >&2; usage 1 ;;
    *)
      if [ -z "$REPO" ]; then REPO="$1"; else echo "Nadmiarowy argument: $1" >&2; usage 1; fi
      ;;
  esac
  shift
done

[ -n "$REPO" ] || { echo "BŁĄD: podaj repozytorium, np. tkogut/osint-lead-tracker" >&2; usage 1; }

PROJECT="${REPO##*/}"
[ -n "$KEY_PATH" ]     || KEY_PATH="$HOME/.ssh/${PROJECT}_deploy"
[ -n "$DEPLOY_PATH" ]  || DEPLOY_PATH="/opt/${PROJECT}"

command -v ssh-keygen  >/dev/null || { echo "BŁĄD: brak ssh-keygen." >&2; exit 1; }
command -v ssh-copy-id >/dev/null || { echo "BŁĄD: brak ssh-copy-id." >&2; exit 1; }
command -v gh          >/dev/null || { echo "BŁĄD: brak gh (GitHub CLI)." >&2; exit 1; }
gh auth status >/dev/null 2>&1   || { echo "BŁĄD: gh nie jest zalogowany (gh auth login)." >&2; exit 1; }

confirm() {
  [ "$ASSUME_YES" -eq 1 ] && return 0
  printf '%s [t/N] ' "$1"
  read -r ans || true
  case "$ans" in [tT][aA][kK]|[tT]|[yY][eE][sS]|[yY]) return 0 ;; *) return 1 ;; esac
}

echo "▶ Repozytorium : $REPO"
echo "▶ VPS          : ${VPS_USER}@${HOST}:${PORT}"
echo "▶ Klucz        : $KEY_PATH"
echo "▶ DEPLOY_PATH  : $DEPLOY_PATH"
echo "▶ Passphrase   : $([ "$USE_PASSPHRASE" -eq 1 ] && echo tak || echo nie)"
echo

# --- 1. Klucz -----------------------------------------------------------------
if [ -f "$KEY_PATH" ]; then
  echo "ℹ️  Klucz już istnieje: $KEY_PATH (użyję go, nie nadpisuję)."
else
  if [ "$USE_PASSPHRASE" -eq 1 ]; then
    echo "🔑 Generuję klucz ed25519 z passphrase..."
    ssh-keygen -t ed25519 -f "$KEY_PATH" -C "github-${PROJECT}"
  else
    echo "🔑 Generuję klucz ed25519 bez passphrase..."
    ssh-keygen -t ed25519 -f "$KEY_PATH" -N "" -C "github-${PROJECT}"
  fi
  chmod 600 "$KEY_PATH" 2>/dev/null || true
fi

# --- 2. Wgranie klucza publicznego na VPS ------------------------------------
echo
confirm "Wgrać klucz publiczny na ${VPS_USER}@${HOST} (ssh-copy-id)?" || { echo "Przerwano."; exit 1; }
ssh-copy-id -p "$PORT" -i "${KEY_PATH}.pub" "${VPS_USER}@${HOST}"

# --- 3. Weryfikacja -----------------------------------------------------------
echo
echo "🧪 Weryfikuję połączenie SSH..."
if ssh -p "$PORT" -i "$KEY_PATH" -o IdentitiesOnly=yes -o BatchMode=yes -o ConnectTimeout=15 \
      "${VPS_USER}@${HOST}" "echo OK && (docker --version || true)"; then
  echo "✅ Połączenie działa."
else
  echo "❌ Weryfikacja SSH nie powiodła się — sprawdź klucz i authorized_keys na VPS." >&2
  exit 1
fi

# --- 4. Sekret z kluczem prywatnym -------------------------------------------
echo
confirm "Ustawić sekret VPS_SSH_KEY w repo $REPO?" || { echo "Przerwano."; exit 1; }
gh secret set VPS_SSH_KEY --repo "$REPO" < "$KEY_PATH"
echo "✅ VPS_SSH_KEY ustawiony."

if [ "$USE_PASSPHRASE" -eq 1 ]; then
  echo "🔐 Ustawiam VPS_SSH_PASSPHRASE (wpisz hasło klucza w promptcie):"
  gh secret set VPS_SSH_PASSPHRASE --repo "$REPO"
  echo "✅ VPS_SSH_PASSPHRASE ustawiony."
fi

# --- 5. Zmienne repo (host / ścieżka) ----------------------------------------
echo
if confirm "Ustawić zmienne repo VPS_HOST i DEPLOY_PATH?"; then
  gh variable set VPS_HOST    --repo "$REPO" --body "$HOST"
  gh variable set DEPLOY_PATH --repo "$REPO" --body "$DEPLOY_PATH"
  echo "✅ Zmienne ustawione."
fi

# --- 6. Podsumowanie ----------------------------------------------------------
echo
echo "📋 Sekrety w $REPO:"
gh secret list --repo "$REPO" || true
echo
echo "🚀 Gotowe. Uruchom deploy:  gh workflow run deploy.yml --repo $REPO"
echo "   (workflow musi już istnieć na gałęzi domyślnej)"
