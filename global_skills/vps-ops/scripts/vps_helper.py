#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
import re

# Konfiguracja VPS
VPS_HOST = "srv1490214.hstgr.cloud"
VPS_USER = "root"

def find_ssh_auth_sock():
    """Próbuje automatycznie odnaleźć aktywny socket ssh-agent w katalogu /tmp."""
    if "SSH_AUTH_SOCK" in os.environ and os.path.exists(os.environ["SSH_AUTH_SOCK"]):
        return os.environ["SSH_AUTH_SOCK"]
    
    try:
        tmp_dirs = os.listdir("/tmp")
        for d in tmp_dirs:
            if d.startswith("ssh-"):
                agent_dir = os.path.join("/tmp", d)
                if os.path.isdir(agent_dir):
                    for f in os.listdir(agent_dir):
                        if f.startswith("agent."):
                            sock_path = os.path.join(agent_dir, f)
                            return sock_path
    except Exception:
        pass
    return None

def run_ssh_command(cmd, ssh_sock=None):
    """Uruchamia komendę przez SSH na VPS."""
    env = os.environ.copy()
    if ssh_sock:
        env["SSH_AUTH_SOCK"] = ssh_sock
        
    ssh_cmd = [
        "ssh", 
        "-o", "StrictHostKeyChecking=no", 
        "-o", "ConnectTimeout=15",
        f"{VPS_USER}@{VPS_HOST}", 
        cmd
    ]
    
    result = subprocess.run(ssh_cmd, env=env, capture_output=True, text=True)
    return result

def cmd_status(args, ssh_sock):
    """Wyświetla ogólny status zasobów VPS oraz listę kontenerów docker."""
    print("🪐 Pobieranie statusu z VPS...")
    
    # Status Docker
    print("\n--- Status Kontenerów Docker ---")
    res_docker = run_ssh_command("docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'", ssh_sock)
    if res_docker.returncode == 0:
        print(res_docker.stdout.strip())
    else:
        print(f"❌ Nie można pobrać statusu docker: {res_docker.stderr}")
        sys.exit(1)
        
    # Status Zasobów Systemowych
    print("\n--- Zużycie Pamięci RAM ---")
    res_ram = run_ssh_command("free -h", ssh_sock)
    if res_ram.returncode == 0:
        print(res_ram.stdout.strip())
        
    print("\n--- Miejsce na Dysku ---")
    res_disk = run_ssh_command("df -h /", ssh_sock)
    if res_disk.returncode == 0:
        print(res_disk.stdout.strip())

def cmd_deploy(args, ssh_sock):
    """Wdraża aplikację na VPS (git pull + docker compose build & restart)."""
    project_dir = args.dir
    branch = args.branch
    no_prune = args.no_prune
    
    print(f"🪐 [1/4] Rozpoczynam deploy w katalogu VPS: {project_dir} (gałąź: {branch})...")
    
    # 1. Sprawdzenie katalogu projektu i git fetch
    check_cmd = f"cd {project_dir} && git fetch --all"
    res = run_ssh_command(check_cmd, ssh_sock)
    if res.returncode != 0:
        print(f"❌ Błąd: Nie odnaleziono katalogu projektu lub wystąpił błąd git: {res.stderr.strip()}")
        sys.exit(1)
        
    # 2. Git stash (zabezpieczenie lokalnych zmian na VPS)
    print("🪐 [2/4] Zabezpieczanie lokalnych modyfikacji (git stash)...")
    stash_cmd = f"cd {project_dir} && (git diff-index --quiet HEAD -- || git stash)"
    run_ssh_command(stash_cmd, ssh_sock)
    
    # 3. Git checkout & pull
    print(f"🪐 [3/4] Pobieranie najnowszych zmian z gałęzi {branch}...")
    pull_cmd = f"cd {project_dir} && git checkout {branch} && git pull origin {branch}"
    res_pull = run_ssh_command(pull_cmd, ssh_sock)
    if res_pull.returncode != 0:
        print(f"❌ Błąd pull: {res_pull.stderr.strip()}")
        sys.exit(1)
    print(res_pull.stdout.strip())
    
    # 4. Docker Compose Rebuild
    print("🪐 [4/4] Przebudowa i restart kontenerów w tle...")
    compose_cmd = f"cd {project_dir} && docker compose up -d --build"
    res_compose = run_ssh_command(compose_cmd, ssh_sock)
    if res_compose.returncode != 0:
        print(f"❌ Błąd docker compose: {res_compose.stderr.strip()}")
        sys.exit(1)
    print(res_compose.stdout.strip())
    
    # Prune
    if not no_prune:
        print("🧹 Czyszczenie nieużywanych obrazów docker...")
        run_ssh_command("docker system prune -f", ssh_sock)
        
    print("✅ Wdrożenie zakończone pomyślnie!")
    
    # Weryfikacja statusu
    res_ps = run_ssh_command(f"cd {project_dir} && docker compose ps", ssh_sock)
    if res_ps.returncode == 0:
        print(res_ps.stdout.strip())

def cmd_logs(args, ssh_sock):
    """Pobiera logi z wybranego kontenera lub w katalogu compose."""
    project_dir = args.dir
    container = args.container
    lines = args.lines
    follow = args.follow
    
    env = os.environ.copy()
    if ssh_sock:
        env["SSH_AUTH_SOCK"] = ssh_sock
        
    if container:
        print(f"🪐 Pobieranie ostatnich {lines} linii logów z kontenera: {container}...")
        log_cmd = f"docker logs --tail={lines} {container}"
    elif project_dir:
        print(f"🪐 Pobieranie ostatnich {lines} linii logów dla projektu w: {project_dir}...")
        log_cmd = f"cd {project_dir} && docker compose logs --tail={lines}"
    else:
        print("❌ Błąd: Musisz podać albo katalog compose (--dir), albo nazwę kontenera (--container).")
        sys.exit(1)
        
    if follow:
        # Tryb ciągłego śledzenia wymaga interaktywnego ssh
        print("📺 Śledzenie logów (naciśnij Ctrl+C aby wyjść)...")
        ssh_cmd = ["ssh", "-t", "-o", "StrictHostKeyChecking=no", f"{VPS_USER}@{VPS_HOST}", log_cmd + " -f"]
        subprocess.run(ssh_cmd, env=env)
    else:
        res = run_ssh_command(log_cmd, ssh_sock)
        if res.returncode == 0:
            print(res.stdout.strip())
            if res.stderr.strip():
                print(res.stderr.strip())
        else:
            print(f"❌ Nie można pobrać logów: {res.stderr}")
            sys.exit(1)

def cmd_env(args, ssh_sock):
    """Umożliwia podgląd i modyfikację pliku .env w projekcie na VPS."""
    project_dir = args.dir
    action = args.action
    key = args.key
    value = args.value
    
    env_file_path = f"{project_dir}/.env"
    
    if action == "get":
        print(f"🪐 Odczytywanie pliku .env z: {env_file_path}...")
        res = run_ssh_command(f"cat {env_file_path}", ssh_sock)
        if res.returncode != 0:
            print(f"❌ Nie udało się odczytać pliku .env (może jeszcze nie istnieć?): {res.stderr.strip()}")
            sys.exit(1)
            
        if key:
            # Szukanie konkretnego klucza
            lines = res.stdout.split("\n")
            found = False
            for line in lines:
                if line.startswith(f"{key}="):
                    print(line)
                    found = True
                    break
            if not found:
                print(f"⚠️  Nie znaleziono zmiennej '{key}' w .env.")
        else:
            print(res.stdout.strip())
            
    elif action == "set":
        if not key or not value:
            print("❌ Błąd: Musisz podać --key oraz --value aby ustawić zmienną środowiskową.")
            sys.exit(1)
            
        print(f"🪐 Ustawianie zmiennej '{key}={value}' w {env_file_path}...")
        
        # Pobieramy obecny stan .env
        res = run_ssh_command(f"cat {env_file_path}", ssh_sock)
        env_content = res.stdout if res.returncode == 0 else ""
        
        # Sprawdzamy czy klucz istnieje i modyfikujemy
        lines = env_content.split("\n")
        key_exists = False
        new_lines = []
        
        for line in lines:
            if line.startswith(f"{key}="):
                new_lines.append(f"{key}={value}")
                key_exists = True
            else:
                new_lines.append(line)
                
        if not key_exists:
            if new_lines and new_lines[-1] != "":
                new_lines.append("")
            new_lines.append(f"{key}={value}")
            
        new_env_content = "\n".join(new_lines)
        
        # Zapisujemy nowy plik .env na VPS
        # Używamy base64 aby uniknąć problemów z uciekającymi znakami specjalnymi w bashu
        import base64
        b64_content = base64.b64encode(new_env_content.encode("utf-8")).decode("utf-8")
        
        write_cmd = f"echo '{b64_content}' | base64 -d > {env_file_path}"
        res_write = run_ssh_command(write_cmd, ssh_sock)
        
        if res_write.returncode == 0:
            print(f"✅ Zmienna '{key}' została pomyślnie zaktualizowana.")
        else:
            print(f"❌ Błąd zapisu pliku .env: {res_write.stderr}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="AGENTS-OS VPS Operations Helper CLI")
    parser.add_argument("--sock", help="Ścieżka do socketu SSH_AUTH_SOCK (opcjonalnie)")
    
    subparsers = parser.add_subparsers(dest="command", required=True, help="Dostępne komendy")
    
    # Subparser status
    subparsers.add_parser("status", help="Wyświetla status kontenerów i zasobów VPS")
    
    # Subparser deploy
    parser_deploy = subparsers.add_parser("deploy", help="Wdraża aplikację na VPS (git pull + compose restart)")
    parser_deploy.add_argument("--dir", required=True, help="Katalog projektu na VPS (np. /docker/n8n-g7tq)")
    parser_deploy.add_argument("--branch", default="master", help="Gałąź git (domyślnie: master)")
    parser_deploy.add_argument("--no-prune", action="store_true", help="Pomiń czyszczenie nieużywanych obrazów docker")
    
    # Subparser logs
    parser_logs = subparsers.add_parser("logs", help="Wyświetla logi kontenera lub projektu compose")
    parser_logs.add_argument("--dir", help="Katalog projektu compose na VPS (np. /docker/n8n-g7tq)")
    parser_logs.add_argument("--container", help="Nazwa kontenera na VPS (np. n8n-g7tq-n8n-1)")
    parser_logs.add_argument("--lines", type=int, default=50, help="Liczba linii logów (domyślnie: 50)")
    parser_logs.add_argument("--follow", "-f", action="store_true", help="Śledź logi na żywo (wymaga interaktywnego tty)")
    
    # Subparser env
    parser_env = subparsers.add_parser("env", help="Modyfikuje lub pobiera wartości z pliku .env na VPS")
    parser_env.add_argument("action", choices=["get", "set"], help="Akcja: get (odczyt), set (zapis)")
    parser_env.add_argument("--dir", required=True, help="Katalog projektu na VPS")
    parser_env.add_argument("--key", help="Klucz zmiennej środowiskowej")
    parser_env.add_argument("--value", help="Wartość zmiennej środowiskowej (wymagana przy akcji set)")
    
    args = parser.parse_args()
    
    ssh_sock = args.sock or find_ssh_auth_sock()
    if not ssh_sock:
        print("⚠️  OSTRZEŻENIE: Nie wykryto aktywnego socketu SSH_AUTH_SOCK.")
        print("   Upewnij się, że uruchomiłeś ssh-agent i dodałeś swój klucz SSH (patrz /vps-ops).")
        print("-" * 80)
        
    if args.command == "status":
        cmd_status(args, ssh_sock)
    elif args.command == "deploy":
        cmd_deploy(args, ssh_sock)
    elif args.command == "logs":
        cmd_logs(args, ssh_sock)
    elif args.command == "env":
        cmd_env(args, ssh_sock)

if __name__ == "__main__":
    main()
