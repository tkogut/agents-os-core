---
name: swarm-bootstrapper
description: Automatyczna instancjacja Złotego Standardu AGENTS-OS v4.0 w nowych projektach.
trigger_words: ["@agents.md instantiate", "os-init", "bootstrap", "swarm init"]
version: 1.0
---

# Swarm Bootstrapper (v4.0-AG)

**Goal:** Klonowanie Template Vault (ROOT + LOKAL) do obecnego obszaru roboczego bez niszczenia istniejących repozytoriów.
**Engine:** Caveman Ultra+

## Execution [SEQ-PRO]
Przy wywołaniu komendy, uruchomić skrypt z lokalizacji startowej użytkownika (Target CWD).

**Komenda do wpisania przez Agenta:**
`python3 ~/.gemini/antigravity/skills/swarm-bootstrapper/scripts/bootstrap.py`
