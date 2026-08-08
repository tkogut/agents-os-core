# Raport Refaktoryzacji AGENTS-OS do wersji v5.0.0 Swarm Edition

## 1. Cel i zakres refaktoryzacji
Strategia migracji z `gemini-cli` + `snap` na natywny **Antigravity CLI** (v5.0.0). Powód: wygaśnięcie starych tokenów deweloperskich (18 czerwca 2026 r.).

## 2. Identyfikacja Długu Technologicznego (Legacy Code)
Krytyczne wady `INSTALL.sh` i skryptów:
* **Zależność od Snap:** Brak macOS + Docker/Devcontainers wsparcia. Problemy z linkami ("Snap Sandbox Guard").
* **Przestarzałe CLI:** Użycie `gemini-cli` zamiast wbudowanego Antigravity CLI.
* **Ręczne zarządzanie:** Kopiowanie skilli łamie zasady *Konstytucji AGENTS-OS v5.0*.

## 3. Zrefaktoryzowany Skrypt Inicjalizujący (`INSTALL.sh`)
Przepisać `INSTALL.sh` pod v5.0.0. Usunąć snap, bazować na apt/brew i Antigravity CLI.
*Uwaga: Kod `INSTALL.sh` wdroży autonomicznie agent w pętli wykonawczej.*

## 4. Dalsze Kroki i Rekomendacje dla Architekta
Kroki po wdrożeniu instalatora:
1.  **Weryfikacja `bootstrap.py`:** Poprawne wsparcie `/goal` w nowym CLI.
2.  **Integracja MCP (`mcp_config.json`):** Uruchomienie `antigravity-docs` na macOS bez GUI.
3.  **Audyt:** Testy podatności *Path Traversal* w `os-add-skill`.
