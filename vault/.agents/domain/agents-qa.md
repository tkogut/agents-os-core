# 🛡️ Domain Module: QA & Security Policy

**Reference:** Integrates with [.ai/agentic.config.json](../../.ai/agentic.config.json)

### Validation Policy:
1. **Pytest Gate**: 100% test pass rate required (`52/52 PASSED`).
2. **R-SEC-01 Compliance**: Secrets must be loaded exclusively from `os.getenv()`. Zero hardcoded API keys or passphrases permitted.
3. **Closed Candle Protection**: Indicators (TMA/ATR) must evaluate strictly on `candles[:-1]` to eliminate look-ahead bias.
