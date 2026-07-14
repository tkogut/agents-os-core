#!/usr/bin/env python3
# validate-handshakes.py — Walidacja protokołu handshake subagentów
# Wersja: 5.0-swarm

import os
import sys
import json
import glob

swarm_dir = ".agents/swarm"

if not os.path.exists(swarm_dir):
    print(f"❌ Blad: Katalog {swarm_dir} nie istnieje!")
    sys.exit(1)

handshake_files = glob.glob(os.path.join(swarm_dir, "*_*_handshake.json"))

if not handshake_files:
    print("⚠️  Brak plików handshake w .agents/swarm/. Upewnij sie, ze subagenci zapisali swoje raporty.")
    sys.exit(0)

invalid_count = 0
required_keys = ["conversation_id", "role", "status", "math_consistency_check", "timestamp"]

for file_path in handshake_files:
    print(f"🔍 Walidacja pliku: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        missing = [k for k in required_keys if k not in data]
        if missing:
            print(f"❌ Blad w {file_path}: brakujące klucze {missing}")
            invalid_count += 1
            continue
            
        if data["status"] != "SUCCESS":
            print(f"❌ Blad w {file_path}: status to '{data['status']}', a powinien byc 'SUCCESS'")
            invalid_count += 1
            continue
            
        if data["math_consistency_check"] != "PASSED":
            print(f"❌ Blad w {file_path}: math_consistency_check to '{data['math_consistency_check']}', a powinien byc 'PASSED'")
            invalid_count += 1
            continue
            
        print(f"✅ Plik {file_path} jest POPRAWNY (Rola: {data['role']})")
    except Exception as e:
        print(f"❌ Blad podczas odczytu pliku {file_path}: {e}")
        invalid_count += 1

if invalid_count > 0:
    print(f"❌ Walidacja zakończona niepowodzeniem. Wykryto {invalid_count} blednych raportów handshake!")
    sys.exit(1)

print("🎉 Wszystkie raporty handshake sa poprawne.")
sys.exit(0)
