# .agents/scripts/ — Template Hook Runners

## ⚠️ Zasada Braku Symlinków w Prawdziwym Vaulcie (Zero Symlinks in Vault)
1. **Szablon repozytorium kodowego**: Dowiązanie symboliczne `vault/.agents/scripts/guard_confidential_gemini.py -> ../../scripts/guard_confidential_gemini.py` służy wyłącznie jako fallback ścieżki względnej dla środowiska Antigravity IDE w projektach kodowych.
2. **Prawdziwy Vault Obsidian (`sejf_tk`)**: W produkcyjnym vaulcie (np. `sejf_tk`) **kategorycznie zabrania się stosowania dowiązań symbolicznych (symlinks)**. Wszystkie skrypty lub reguły muszą być fizycznymi, zwykłymi plikami (`regular files`), aby zachować kompatybilność z Obsidian Git, synchronizacją mobilną, systemem Windows i standardem ISO 27001.
