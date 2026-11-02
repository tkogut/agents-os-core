# AGENTS-OS Template Vault Scaffold (v7.0)

Szablon bazowy dystrybuowany do projektów potomnych przez `os-init` i `os-upgrade-project`.

## Zasady Integralności:
1. **Prawdziwy Vault (`sejf_tk`)**: Nigdy nie jest klonowany bezpośrednio do wnętrza projektów kodowych. Projekty posiadają jedynie wskaźnik konfiguracji w `.ai/agentic.config.json` (`context.second_brain.local_path`).
2. **Zakaz Symlinków w Vaulcie**: W vaulcie produkcyjnym nie wolno tworzyć symlinków — wszystkie pliki muszą być fizycznie skopiowane (`regular files`).
3. **Ochrona Poufności (Gemini vs Claude)**: Strażnik PreToolUse `scripts/guard_confidential_gemini.py` zapewnia zgodność z RODO/ISO 27001, blokując odczyt dokumentów `confidential: true` przez modele Gemini bez DPA.
4. **Konfiguracja Ścieżki w Środowiskach Multi-Machine**: Hierarchia rozstrzygania ścieżki vaulta: parametr CLI -> zmienna środowiskowa `OBSIDIAN_VAULT_PATH` -> `.ai/agentic.config.json` (`context.second_brain.local_path`) -> domyślna `/mnt/c/Users/tkogut/Documents/sejf_tk`. Na innej maszynie (np. VPS, inny laptop bez domyślnej ścieżki Windows/WSL) konieczne jest ustawienie `OBSIDIAN_VAULT_PATH` lub wpis w configu. Zgodnie z zasadą Zero Full-Disk Probing brak zdefiniowanej i istniejącej ścieżki skutkuje natychmiastową blokadą dostępu (fail-closed) bez przeszukiwania dysku. Kopie skryptu strażnika w `scripts/` i `.agents/scripts/` muszą być fizycznymi plikami (nie symlinkami) o identycznym hash SHA-256.
