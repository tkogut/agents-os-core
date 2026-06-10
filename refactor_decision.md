# Decyzja Refaktoryzacyjna: Migracja do AGENTS-OS v4.2.1 Swarm Edition

Na podstawie analizy długu technologicznego zawartej w pliku `.agents/specs/raport_refaktoryzacji_v4.2.1-v2.md`, poniżej przedstawiono zestawienie argumentów oraz ocenę ryzyka związanego z migracją do wersji v4.2.1.

---

## 1. Analiza Argumentów (ZA i PRZECIW)

### Lista ZA (Korzyści z migracji):
*   **Wsparcie dla platform (Multi-platform):** Eliminacja sztywnego powiązania ze środowiskiem `snap` pozwala na uruchamianie instalatora na macOS (przez `brew`) oraz w kontenerach Docker i Devcontainers.
*   **Natywne narzędzia:** Zastąpienie wycofywanego `gemini-cli` przez nowe, natywne `Antigravity CLI` (napisane w Go), wspierające nowoczesne protokoły wieloagentowe.
*   **Bezpieczeństwo skilli:** Wdrożenie automatycznego skryptu `os-add-skill` z walidacją nazw zabezpiecza środowisko przed atakami typu *Path Traversal*.
*   **Spójność z Konstytucją:** Przejście na dynamiczny podział ról (Swarm Triad) i automatyczną synchronizację szablonów (The Vault).

### Lista PRZECIW (Koszty i wyzwania):
*   **Prace implementacyjne:** Konieczność przepisania i przetestowania skryptu `INSTALL.sh` na wielu systemach operacyjnych (WSL, Linux, macOS).
*   **Ryzyko regresji:** Potencjalne problemy z kompatybilnością starych skryptów i projektów skonfigurowanych pod `gemini-cli`.
*   **Czas i zasoby:** Wymóg natychmiastowej walidacji i dostosowania silnika `bootstrap.py`.

---

## 2. Ryzyko Braku Migracji przed 18 czerwca 2026 r.

**Termin krytyczny:** 18 czerwca 2026 r. (wygaszenie starych tokenów deweloperskich Google).

W przypadku zaniechania migracji przed tym terminem, system zderzy się z następującymi konsekwencjami:
1.  **Paraliż uwierzytelniania:** Stare narzędzie `gemini-cli` straci możliwość autoryzacji sesji. Wszystkie polecenia odpytujące API modeli Gemini zakończą się błędem autoryzacji.
2.  **Blokada automatyzacji:** Brak możliwości pobierania skilli, aktualizacji dokumentacji MCP oraz synchronizacji szablonów przez `os-init` i `os-add-skill`.
3.  **Całkowity przestój roju:** Zablokowanie komunikacji wewnątrz Swarm Triad (modele Coordinator, Builder i Auditor stracą dostęp do backendu Gemini).

---
*Dokument wygenerowany autonomicznie zgodnie z regułą caveman i rebuild-skill. Status: Zapisano.*
