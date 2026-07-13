#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
import json
import re

# Konfiguracja VPS
VPS_HOST = "srv1490214.hstgr.cloud"
VPS_USER = "root"

# Mapowanie instancji n8n
INSTANCES = {
    "g7tq": {
        "container": "n8n-g7tq-n8n-1",
        "url": "https://n8n-g7tq.srv1490214.hstgr.cloud"
    },
    "pkogut": {
        "container": "n8n-pkogut-n8n-1",
        "url": "https://n8n-pkogut.srv1490214.hstgr.cloud"
    }
}

def find_ssh_auth_sock():
    """Próbuje automatycznie odnaleźć aktywny socket ssh-agent w katalogu /tmp."""
    if "SSH_AUTH_SOCK" in os.environ and os.path.exists(os.environ["SSH_AUTH_SOCK"]):
        return os.environ["SSH_AUTH_SOCK"]
    
    # Przeszukiwanie katalogu /tmp w poszukiwaniu socketów agenta
    try:
        tmp_dirs = os.listdir("/tmp")
        for d in tmp_dirs:
            if d.startswith("ssh-"):
                agent_dir = os.path.join("/tmp", d)
                if os.path.isdir(agent_dir):
                    for f in os.listdir(agent_dir):
                        if f.startswith("agent."):
                            sock_path = os.path.join(agent_dir, f)
                            # Zwróć pierwszy działający gniazdo
                            return sock_path
    except Exception:
        pass
    return None

def run_ssh_command(cmd, ssh_sock=None):
    """Uruchamia komendę przez SSH na VPS z przekazanym agentem SSH."""
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

def run_scp_to_vps(local_path, remote_path, ssh_sock=None):
    """Przesyła plik na VPS za pomocą scp."""
    env = os.environ.copy()
    if ssh_sock:
        env["SSH_AUTH_SOCK"] = ssh_sock
        
    scp_cmd = [
        "scp",
        "-o", "StrictHostKeyChecking=no",
        local_path,
        f"{VPS_USER}@{VPS_HOST}:{remote_path}"
    ]
    result = subprocess.run(scp_cmd, env=env, capture_output=True, text=True)
    return result

def cmd_list(args, ssh_sock):
    """Wyświetla status i informacje o kontenerach n8n na VPS."""
    print("🪐 Pobieranie statusu kontenerów z VPS...")
    res = run_ssh_command("docker ps --format '{{.Names}}\t{{.Status}}\t{{.Ports}}'", ssh_sock)
    if res.returncode != 0:
        print(f"❌ Błąd połączenia z VPS: {res.stderr}")
        sys.exit(1)
        
    lines = res.stdout.strip().split("\n")
    found_any = False
    
    print("\n--- Aktywne Instancje n8n na VPS ---")
    print(f"{'Instancja':<12} | {'Nazwa Kontenera':<20} | {'Status':<15} | {'Adres URL'}")
    print("-" * 80)
    
    for key, data in INSTANCES.items():
        status = "OFFLINE"
        for line in lines:
            if data["container"] in line:
                status = "RUNNING"
                parts = line.split("\t")
                if len(parts) > 1:
                    status = f"RUNNING ({parts[1]})"
                break
        print(f"{key:<12} | {data['container']:<20} | {status:<15} | {data['url']}")
        found_any = True
        
    if not found_any:
        print("Nie znaleziono żadnych działających kontenerów n8n.")

def cmd_export(args, ssh_sock):
    """Eksportuje określony workflow z VPS do pliku lokalnego."""
    instance = args.instance
    workflow_id = args.id
    output_path = args.output
    
    if instance not in INSTANCES:
        print(f"❌ Błąd: Nieprawidłowa instancja. Wybierz spośród: {list(INSTANCES.keys())}")
        sys.exit(1)
        
    container = INSTANCES[instance]["container"]
    print(f"🪐 Eksportowanie workflow '{workflow_id}' z instancji '{instance}' ({container})...")
    
    # Wywołanie eksportu wewnątrz kontenera na VPS
    remote_cmd = f"docker exec -i {container} n8n export:workflow --id={workflow_id}"
    res = run_ssh_command(remote_cmd, ssh_sock)
    
    if res.returncode != 0:
        print(f"❌ Błąd podczas eksportu workflow: {res.stderr.strip() or res.stdout.strip()}")
        sys.exit(1)
        
    # Zapis do pliku lokalnego
    try:
        # Sprawdzamy czy to poprawny JSON
        json_data = json.loads(res.stdout)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Workflow pomyślnie wyeksportowany i zapisany w: {output_path}")
    except json.JSONDecodeError:
        print(f"❌ Błąd: Serwer nie zwrócił poprawnego formatu JSON. Zwrócona treść:\n{res.stdout}")
        sys.exit(1)

def cmd_import(args, ssh_sock):
    """Importuje lokalny plik workflow do n8n na VPS."""
    instance = args.instance
    file_path = args.file
    
    if instance not in INSTANCES:
        print(f"❌ Błąd: Nieprawidłowa instancja. Wybierz spośród: {list(INSTANCES.keys())}")
        sys.exit(1)
        
    if not os.path.exists(file_path):
        print(f"❌ Błąd: Lokalny plik '{file_path}' nie istnieje.")
        sys.exit(1)
        
    # Walidacja pliku JSON pod kątem struktury n8n
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            wf = json.load(f)
            
        # Zabezpieczenie przed brakującym ID w n8n CLI
        if isinstance(wf, dict):
            if "id" not in wf or not wf["id"]:
                # Generujemy tymczasowe ID, jeśli brakuje
                wf["id"] = "IMPORT" + os.urandom(6).hex().upper()
                print(f"⚠️  Brak pola 'id' w pliku. Wygenerowano tymczasowe ID: {wf['id']}")
                # Nadpisujemy tymczasowo plik z dodanym ID do wysyłki
                temp_file = file_path + ".tmp"
                with open(temp_file, "w", encoding="utf-8") as tf:
                    json.dump(wf, tf, indent=2)
                file_path = temp_file
    except Exception as e:
        print(f"❌ Błąd walidacji pliku JSON: {e}")
        sys.exit(1)

    container = INSTANCES[instance]["container"]
    filename = os.path.basename(file_path)
    remote_tmp_path = f"/tmp/{filename}"
    
    print(f"🪐 [1/3] Przesyłanie pliku {filename} na VPS...")
    res = run_scp_to_vps(file_path, remote_tmp_path, ssh_sock)
    
    # Sprzątanie lokalnego pliku tymczasowego
    if file_path.endswith(".tmp"):
        os.remove(file_path)
        
    if res.returncode != 0:
        print(f"❌ Błąd przesyłania pliku: {res.stderr}")
        sys.exit(1)
        
    print(f"🪐 [2/3] Kopiowanie pliku do wnętrza kontenera {container}...")
    cp_cmd = f"docker cp {remote_tmp_path} {container}:{remote_tmp_path}"
    res = run_ssh_command(cp_cmd, ssh_sock)
    if res.returncode != 0:
        print(f"❌ Błąd kopiowania do kontenera: {res.stderr}")
        sys.exit(1)
        
    print(f"🪐 [3/3] Importowanie workflow w n8n...")
    import_cmd = f"docker exec -i {container} n8n import:workflow --input={remote_tmp_path}"
    res = run_ssh_command(import_cmd, ssh_sock)
    
    # Sprzątanie na VPS
    cleanup_cmd = f"rm -f {remote_tmp_path} && docker exec -i {container} rm -f {remote_tmp_path}"
    run_ssh_command(cleanup_cmd, ssh_sock)
    
    if res.returncode != 0:
        print(f"❌ Błąd importowania: {res.stderr.strip() or res.stdout.strip()}")
        sys.exit(1)
        
    print(res.stdout.strip())
    print(f"✅ Pomyślnie zaimportowano workflow do instancji '{instance}'.")

def cmd_backup(args, ssh_sock):
    """Tworzy kopię zapasową wszystkich workflowów z danej instancji."""
    instance = args.instance
    backup_dir = args.dir
    
    if instance not in INSTANCES:
        print(f"❌ Błąd: Nieprawidłowa instancja. Wybierz spośród: {list(INSTANCES.keys())}")
        sys.exit(1)
        
    container = INSTANCES[instance]["container"]
    os.makedirs(backup_dir, exist_ok=True)
    
    print(f"🪐 Pobieranie listy workflowów z instancji '{instance}'...")
    # Wywołanie n8n export do stdout jako cała tablica
    res = run_ssh_command(f"docker exec -i {container} n8n export:workflow --all", ssh_sock)
    
    if res.returncode != 0:
        print(f"❌ Błąd pobierania danych: {res.stderr}")
        sys.exit(1)
        
    try:
        workflows = json.loads(res.stdout)
        if not isinstance(workflows, list):
            workflows = [workflows]
            
        print(f"Znaleziono {len(workflows)} workflowów. Zapisywanie...")
        for wf in workflows:
            wf_id = wf.get("id", "unknown")
            name = wf.get("name", "unnamed").replace(" ", "_")
            # Usuwanie znaków specjalnych z nazwy pliku
            name = re.sub(r'[\\/*?:"<>|]', "", name)
            
            output_file = os.path.join(backup_dir, f"{wf_id}_{name}.json")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(wf, f, indent=2, ensure_ascii=False)
            print(f"   💾 Zapisano: {wf_id}_{name}.json")
            
        print(f"✅ Pomyślnie wykonano kopie zapasowe w katalogu: {backup_dir}")
    except Exception as e:
        print(f"❌ Błąd podczas zapisu kopii zapasowych: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="AGENTS-OS n8n Helper CLI")
    parser.add_argument("--sock", help="Ścieżka do socketu SSH_AUTH_SOCK (opcjonalnie)")
    
    subparsers = parser.add_subparsers(dest="command", required=True, help="Dostępne komendy")
    
    # Subparser list
    subparsers.add_parser("list", help="Wyświetla status kontenerów n8n na VPS")
    
    # Subparser export
    parser_export = subparsers.add_parser("export", help="Eksportuje workflow z VPS")
    parser_export.add_argument("--instance", required=True, choices=list(INSTANCES.keys()), help="Nazwa instancji (g7tq/pkogut)")
    parser_export.add_argument("--id", required=True, help="ID workflow do pobrania")
    parser_export.add_argument("--output", required=True, help="Ścieżka docelowa pliku .json lokalnie")
    
    # Subparser import
    parser_import = subparsers.add_parser("import", help="Importuje plik workflow na VPS")
    parser_import.add_argument("--instance", required=True, choices=list(INSTANCES.keys()), help="Nazwa instancji (g7tq/pkogut)")
    parser_import.add_argument("--file", required=True, help="Ścieżka do lokalnego pliku .json z workflowem")
    
    # Subparser backup
    parser_backup = subparsers.add_parser("backup", help="Robi backup wszystkich workflowów z VPS")
    parser_backup.add_argument("--instance", required=True, choices=list(INSTANCES.keys()), help="Nazwa instancji (g7tq/pkogut)")
    parser_backup.add_argument("--dir", default="./n8n_backups", help="Katalog zapisu kopii zapasowych")
    
    args = parser.parse_args()
    
    # Wykrywanie socketu agenta SSH
    ssh_sock = args.sock or find_ssh_auth_sock()
    if not ssh_sock:
        print("⚠️  OSTRZEŻENIE: Nie wykryto aktywnego socketu SSH_AUTH_SOCK.")
        print("   Upewnij się, że uruchomiłeś ssh-agent i dodałeś swój klucz SSH (patrz /vps-ops).")
        print("   Możesz też podać go ręcznie używając flagi --sock.")
        print("-" * 80)
    
    if args.command == "list":
        cmd_list(args, ssh_sock)
    elif args.command == "export":
        cmd_export(args, ssh_sock)
    elif args.command == "import":
        cmd_import(args, ssh_sock)
    elif args.command == "backup":
        cmd_backup(args, ssh_sock)

if __name__ == "__main__":
    main()
