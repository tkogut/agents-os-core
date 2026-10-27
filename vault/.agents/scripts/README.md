# .agents/scripts/ — Template Hook Runners

## ⚠️ Zasada Braku Symlinków (Zero Symlinks Mandate)
1. **Szablon repozytorium kodowego**: Plik `vault/.agents/scripts/guard_confidential_gemini.py` jest zwykłą, fizyczną kopią (nie symlinkiem), zsynchronizowaną z `vault/scripts/guard_confidential_gemini.py` oraz `scripts/guard_confidential_gemini.py`. Służy jako bezpośrednia ścieżka uruchomieniowa dla środowiska Antigravity IDE.
2. **Prawdziwy Vault Obsidian (`sejf_tk`)**: W produkcyjnym vaulcie (np. `sejf_tk`) **kategorycznie zabrania się stosowania dowiązań symbolicznych (symlinks)**. Wszystkie skrypty lub reguły muszą być fizycznymi, zwykłymi plikami (`regular files`), aby zachować 100% kompatybilność z Obsidian Git, synchronizacją mobilną, systemem Windows i standardem ISO 27001.
