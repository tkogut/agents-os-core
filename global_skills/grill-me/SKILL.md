---
name: grill-me
description: Pre-flight architectural interview protocol before code implementation. Generates rigorous architectural questions covering multi-machine sync, database fail-safes, edge cases, and state-dump consistency.
trigger: /grill-me
---

# 🛸 Grill-Me Architectural Pre-Flight Protocol

Wykonaj protokół wywiadu architektonicznego przed przystąpieniem do implementacji zadań:

```bash
node .agents/skills/grill-me.js || python3 .agents/skills/grill-me/scripts/grill_me.py
```

## Zasady Protokołu (Mandate)
1. **Wywiad przed kodowaniem**: Każde nowe zadanie dotykające architektury, bazy danych lub synchronizacji rozproszonej wymaga odpowiedzi na 5 pytań kontrolnych.
2. **Utrwalenie w pamięci**: Odpowiedzi i kluczowe ustalenia muszą zostać wpisane do `.agents/MEMORY.md` w sekcji `## 📝 Decisions & Key Milestones`.
3. **Weryfikacja przez Auditora**: Auditor weryfikuje zgodność implementacji z ustaleniami zapisanymi podczas sesji grill-me.
