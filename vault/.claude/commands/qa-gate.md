# /qa-gate — Run QA Gate Before PR
#
# Usage: /qa-gate
# Runs all QA checks required by SDLC Phase 5 before creating a PR.

Run the full QA Gate for this project. Report PASS/FAIL for each gate.

Execute in sequence:

## Gate 1: Shell Lint
```bash
echo "=== GATE 1: shellcheck ==="
shellcheck scripts/*.sh 2>&1 && echo "✅ PASS" || echo "❌ FAIL"
```

## Gate 2: Python Typecheck
```bash
echo "=== GATE 2: py_compile ==="
python3 -m py_compile scripts/*.py && echo "✅ PASS" || echo "❌ FAIL"
```

## Gate 3: Handshake Validation
```bash
echo "=== GATE 3: validate-handshakes ==="
python3 scripts/validate-handshakes.py 2>&1 && echo "✅ PASS" || echo "❌ FAIL"
```

## Gate 4: Integration Test (optional, slow)
```bash
echo "=== GATE 4: test_bootstrap ==="
bash execution/test_bootstrap.sh 2>&1 | tail -5
```

After all gates:
- ALL PASS → "✅ QA Gate cleared. Ready for PR."
- ANY FAIL → "❌ QA Gate BLOCKED. Fix issues before PR."

Policy: NO PR without Gate 1 + Gate 2 + Gate 3 passing.
