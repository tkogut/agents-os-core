# Plan adaptacji mechanizmów inspirowanych PWF

**Data:** 2026-09-16
**Autor:** Builder (Claude Opus 5), przegląd adversarial rekomendacji Sonnet 5
**Status:** Faza 0 wdrożona. Faza 1 warunkowa (wymaga pomiaru). Faza 2 zablokowana (wymaga oceny dostawcy).
**Przedmiot:** skill `planning-with-files` (OthmanAdi, MIT) — github.com/OthmanAdi/planning-with-files

---

## 1. Werdykt i kontekst

**NIE BRAĆ PWF TERAZ.** Kolejność jest odwrotna niż proponowano: najpierw naprawić własne, potem oceniać cudze.

Uzasadnienie skrótowe:

| Delta PWF | Werdykt |
|---|---|
| D1 per-turn injection | ~80% uzyskane własnym `UserPromptSubmit` (Faza 0) |
| D2 PreCompact snapshot | 100% uzyskane własnym hookiem (Faza 0) |
| D3 maszynowy gate | zbudować samemu — godziny pracy, zero dostawcy (Faza 1) |
| D4 ledger per-agent | zbudować samemu — `echo >> plik` (Faza 1) |
| D5 PLAN_ID / izolacja worktree | **odłożone** — problem dziś nie istnieje operacyjnie |
| D6 attestation SHA-256 | **odrzucone jako gorsze niż nic** — zastąpione podpisami commitów |

Po Fazie 0 zostaje ~1 delta o niepewnej wartości, przeciw kosztowi: wykonywanie
obcego kodu na każdym wywołaniu narzędzia, w repozytorium, które **dystrybuuje
skille do projektów klienckich**, pod rygorem ISO 27001. Rachunek nie wychodzi.

Dowody w README PWF (13.3→5.0 tur, 3/3, 5/5, 96.7% pass rate) to deklaracje autora
narzędzia mierzącego własne narzędzie, przy n=3 i n=5. 26929 gwiazdek przy repo
utworzonym 2026-01-03 to sygnał popularności, nie audytu. Wersja 3.18.2 w 8 miesięcy
≈ release co ~5 dni — interfejs niestabilny, vendorowanie zamienia to na dług.

### Co już zrobiono (Faza 0, branch `feature/pwf-review-fixes`)

| Id | Zmiana | Plik |
|---|---|---|
| A1 | usunięty `merge=union` z plików checklistowych `task.md`; migracja w generatorze | `.gitattributes`, `vault/.gitattributes`, `os-upgrade-project` |
| A2 | hooki swarmu faktycznie podpięte do Claude Code + `UserPromptSubmit` (D1) + `PreCompact` (D2) | `.claude/settings.json`, `.agents/hooks/*.sh` |
| A3 | podpisy commitów zamiast attestation (D6) — dokumentacja, decyzje serwerowe otwarte | `.agents/specs/commit-signing.md`, `SDLC.md` |
| A4 | pinning refów + weryfikacja SHA-256 + fail-closed staging | `os-add-skill` |

---

## 2. Kryterium wejścia do Fazy 1 (pomiar, nie przeczucie)

Faza 1 rusza **tylko jeśli** problem re-orientacji utrzymuje się PO wdrożeniu A2.
Bez własnego pomiaru kupujemy lek na chorobę zdiagnozowaną przez sprzedawcę leku.

**Protokół pomiaru — 10 kolejnych sesji roboczych:**

1. Licznik automatyczny: hook `UserPromptSubmit` już emituje linię `[SWARM] ...`.
   Dopisać do niego zliczanie do `.agents/swarm/reground-usage.jsonl`
   (1 rekord na turę: `{ts, branch, dirty, open, done}`).
2. Licznik ręczny: operator odnotowuje każdy przypadek, w którym **musiał** ręcznie
   przypomnieć agentowi stan zadania ("gdzie jesteśmy", "przeczytaj task.md",
   ponowne wklejenie planu).
3. Odnotować każdą kompakcję i to, czy po niej agent poprawnie odtworzył stan
   z `.agents/swarm/precompact-snapshot.md`.

**Próg decyzyjny:**

- ≥ 3 ręczne re-orientacje na 10 sesji **lub** ≥ 1 utrata stanu po kompakcji → uruchom Fazę 1.
- poniżej progu → **nie budować nic więcej**. Faza 0 wystarczyła; zamknąć temat.

Pomiar bez progu ustalonego z góry jest nieuczciwy — próg jest zapisany tutaj przed pomiarem.

---

## 3. Faza 1 — własna implementacja D3 i D4

Warunek: próg z §2 przekroczony. Zero zależności zewnętrznych.

### 3.1 D3 — `check-complete.sh`, maszynowy gate zamiast prozy

**Problem:** dziś "ukończenie" jest samooceną modelu zapisaną prozą w `task.md`
(„Status: COMPLETE"). Nic tego nie weryfikuje.

**Rozwiązanie:** `scripts/check-complete.sh` — exit code, nie narracja.

```
scripts/check-complete.sh [--task .agents/task.md] [--strict]
  exit 0  wszystkie pozycje checklisty zamknięte i bramki QA przeszły
  exit 1  pozostały otwarte pozycje `- [ ]`  (wypisuje je)
  exit 2  checklista zamknięta, ale bramka QA padła
  exit 3  brak/nieczytelny task.md  (w --strict; bez --strict => exit 0 + warning)
```

Zakres kontroli:
1. brak linii `- [ ]` w `.agents/task.md`,
2. brak niescommitowanych zmian w `.agents/` (stan zsynchronizowany),
3. `python3 scripts/validate-handshakes.py` przechodzi,
4. handshake dla bieżącego `conversation_id` istnieje i ma `status: SUCCESS`.

**Kto uruchamia:** Auditor w Fazie 5 SDLC (QA Gate), oraz `/qa-gate` lokalnie.
**Czego NIE robi:** nie blokuje eventu `Stop`. Patrz §5 — kolizja z auto-syncem.

### 3.2 D4 — append-only ledger per rola

**Problem:** dziś jeden handshake JSON = snapshot na koniec sesji. Zero śladu przebiegu,
zero rozróżnienia kto co zrobił, brak możliwości rekonstrukcji po awarii.

**Rozwiązanie:** `.agents/swarm/ledger-<rola>.jsonl` — append-only, 1 linia = 1 zdarzenie.

```jsonl
{"ts":"2026-09-16T12:04:11Z","role":"builder","session":"9aa1a841","event":"phase_start","phase":"A1","ref":"feature/pwf-review-fixes"}
{"ts":"2026-09-16T12:06:02Z","role":"builder","session":"9aa1a841","event":"commit","sha":"1bfddbf","subject":"fix(sync): drop union merge on checklist task.md"}
{"ts":"2026-09-16T12:31:40Z","role":"auditor","session":"c71f02aa","event":"gate","result":"PASS","gate":"check-complete"}
```

Pola obowiązkowe: `ts` (UTC ISO-8601), `role`, `session`, `event`. Reszta zależna od `event`.
Słownik `event`: `phase_start` | `phase_done` | `commit` | `gate` | `block` | `handoff` | `note`.

| Rola | Pisze do | Czyta |
|---|---|---|
| Coordinator | `ledger-coordinator.jsonl` | wszystkie trzy |
| Builder | `ledger-builder.jsonl` | własny + coordinator |
| Auditor | `ledger-auditor.jsonl` | wszystkie trzy |

**Zasada twarda: każda rola pisze WYŁĄCZNIE do swojego pliku.** To eliminuje split-brain
przy równoległych maszynach: dwa niezależne dopisy do różnych plików nigdy nie konfliktują.

**`.gitattributes`:** pliki `ledger-*.jsonl` są **prawdziwie append-only** (żadna linia nie
jest nigdy aktualizowana), więc `merge=union` jest dla nich **poprawne** — w przeciwieństwie
do `task.md`. Do dopisania przy wdrożeniu Fazy 1, wraz z komentarzem wyjaśniającym różnicę.

**Integracja z handshake (nie zastąpienie):** handshake pozostaje kontraktem przejścia faz
SDLC (Faza 4 → Faza 5). Ledger to dziennik przebiegu. `generate-handshake.py` dostaje
pole `ledger_lines` — liczbę zdarzeń roli w sesji — żeby handshake bez śladu w ledgerze
był wykrywalny jako podejrzany.

**Rotacja:** przy > 5000 linii archiwizacja do `.agents/swarm/archive/ledger-<rola>-<rrrr-mm>.jsonl`.

---

## 4. D5 — odłożone, z kryterium ponownej oceny

PLAN_ID / `PWF_PLAN_ROOT` rozwiązują kolizję planów między równoległymi worktree.

**Stan faktyczny (zweryfikowany 2026-09-16):** `git worktree list` pokazuje **wyłącznie
główne repozytorium**. Zero worktree, mimo że `.agents/task.md` deklaruje
`Worktree: tmp/worktrees/fix/hook-branch-protection`. Mandat SDLC jest aspiracyjny.

Dodatkowo problem, który D5 miał rozwiązać w wariancie checklistowym, został rozwiązany
za darmo w A1 (usunięcie `merge=union` z `task.md`).

**Kryterium ponownej oceny:** ≥ 2 worktree żyjące równocześnie dłużej niż jedna sesja,
**lub** pierwszy realny konflikt na `.agents/task.md` między worktree. Do tego czasu:
nie budować, nie wdrażać.

---

## 5. Faza 2 — warunkowa adopcja PWF (checklista blokująca)

Żadna pozycja poniżej nie jest opcjonalna. **Do odhaczenia PRZED jakimkolwiek
dodaniem PWF do `global_skills/`, `INSTALL.sh`, `os-init` lub `vault/`.**

### 5.1 Ocena dostawcy (ISO 27001 A.5.19–A.5.23, A.8.30)
- [ ] Wpis w rejestrze dostawców: nazwa, właściciel upstream, kanał kontaktu bezpieczeństwa.
- [ ] Udokumentowany brak SLA i model jednego maintainera — zaakceptowany pisemnie przez właściciela ryzyka.
- [ ] Decyzja: czy jeden maintainer bez security contact w ogóle przechodzi naszą ocenę dostawcy.

### 5.2 Pinning i integralność
- [ ] Vendorowanie do `.agents/skills/planning-with-files/` przypięte do **konkretnego commit SHA** (nie tagu, nie gałęzi).
- [ ] SHA zapisany w `.skill-lock.json` (mechanizm gotowy — A4).
- [ ] Instalacja przechodzi przy `AGENTS_OS_REQUIRE_PIN=1`.
- [ ] **Uwaga:** `.agents/skills/` jest w `.gitignore` — vendorowana kopia NIE będzie commitowana. Rozstrzygnąć: wyjątek w `.gitignore` czy inna lokalizacja. Bez tego „przypięta kopia" nie istnieje na innych maszynach.

### 5.3 Ograniczenie powierzchni wykonania
- [ ] `PreToolUse` i `PostToolUse` **wyłączone**. Bezwarunkowo.
      Powód: hook widzi `tool_input` każdego Write/Edit/Bash, czyli treść zapisywanych plików
      i komend — pełny kanał eksfiltracji, jeden złośliwy commit upstream od aktywacji.
      Jest to wprost sprzeczne z `CLAUDE.md` §6 (R-SEC-01), który zabrania agentowi nawet
      *czytać* `.env`.
- [ ] Dozwolone wyłącznie `UserPromptSubmit` i `PreCompact`.
- [ ] Tryb `gated` **nigdy** na evencie `Stop`, na którym działa nasz auto-sync.
      Powód: nasz `Stop` jest fail-open z definicji (`|| true`, `2>/dev/null`, zawsze exit 0),
      gate PWF jest fail-closed i potrzebuje exit code. Hooki na jednym evencie działają
      sekwencyjnie, nie ekskluzywnie: każdy zablokowany `Stop` zdąży wykonać commit+push
      stanu pośredniego. Przy `cap = 20` to do 20 śmieciowych pushy na sesję.
      To niezgodność projektowa, nie parametr do ustawienia.

### 5.4 Licencja i własność
- [ ] `LICENSE` / `NOTICE` z tekstem MIT i atrybucją w vendorowanej kopii.
- [ ] Atrybucja w dokumentacji dystrybucji (`README.md` / `docs/API.md`) — repo redystrybuuje skille do projektów klienckich.
- [ ] **Imienny właściciel** vendorowanej kopii (osoba, nie rola).
- [ ] Kadencja przeglądu diffa upstream: **kwartalnie**, wpisane do kalendarza.
      Przy tempie ~1 release / 5 dni kopia bez właściciela zgnije w miesiąc.

### 5.5 Blast radius
- [ ] Decyzja świadoma: czy PWF trafia tylko do `agents-os-core`, czy do **wszystkich**
      projektów downstream przez `INSTALL.sh` / `os-init` / `global_skills/`.
- [ ] Jeśli downstream — zgoda właściciela ryzyka na dystrybucję obcego kodu wykonywanego
      przez agenta do projektów klienckich.

**Jeśli którakolwiek pozycja pozostaje nieodhaczona — PWF pozostaje wyłącznie
czytanym wzorcem projektowym (SKILL.md jako dokumentacja), bez wykonywania kodu.**

---

## 6. Otwarte findingi ISO 27001 (niezależne od PWF)

Wykryte przy okazji przeglądu. **Priorytet wyższy niż cała dyskusja o PWF** — dotyczą
stanu faktycznego, nie hipotetycznej adopcji.

| Id | Finding | Stan |
|---|---|---|
| I1 | `os-add-skill` ściągał kod z dwóch repozytoriów GitHub (w tym obcego `sickn33/antigravity-awesome-skills`) z HEAD gałęzi domyślnej, bez pinowania i bez weryfikacji integralności; błędy pobrania były połykane, więc częściowy install raportował sukces | **ZAMKNIĘTE** przez A4 (pinning, SHA-256, lock, staging, fail-closed `--strict`) |
| I2 | Blast radius: repo nie jest aplikacją, tylko **dystrybutorem skilli** (`INSTALL.sh`, `os-init`, `os-init-claude`, `os-upgrade-project`, `global_skills/` = 48 skilli, `vault/`). Każda decyzja o skillu propaguje się do projektów downstream | **OTWARTE** — wymaga decyzji właściciela ryzyka, nie zmiany w kodzie |
| I3 | Sprzeczność R-SEC-01 vs hooki widzące `tool_input`: `CLAUDE.md` §6 zabrania czytania `.env`, a hooki `PreToolUse` dowolnego skilla widzą treść każdego Write/Edit/Bash | **OTWARTE** — do rozstrzygnięcia jako polityka: czy obce hooki narzędziowe są w ogóle dopuszczalne |
| I4 | Brak kontroli integralności stanu swarmu synchronizowanego między maszynami (`MEMORY.md`, `task.md`) | **CZĘŚCIOWO** — procedura i decyzje w `.agents/specs/commit-signing.md` (A3); wymaga działania użytkownika na każdej maszynie |
| I5 | `master` bez branch protection; repo **publiczne**, własność konta User | **OTWARTE** — decyzja użytkownika, nie wykonano żadnej zmiany w GitHub |
| I6 | Brak niezależnego procesu przeglądu dla ~69 skilli już zainstalowanych w `.claude/skills/` | **OTWARTE** — poprzeczka podniesiona dla nowych (A4); istniejące nieprzejrzane |

**Rekomendacja priorytetyzacji:** I2 i I3 przed jakąkolwiek dalszą pracą nad PWF.
Obie są decyzjami politycznymi, nie inżynierskimi, i obie determinują, czy Faza 2
ma w ogóle sens. I1 zamknięte. I4 i I5 wymagają jednego działania użytkownika każde.

---

## 7. Warunki ponownego otwarcia tematu PWF

Temat wraca na stół **tylko** gdy:
1. próg pomiaru z §2 przekroczony **i** Faza 1 wdrożona **i** nadal niewystarczająca, **lub**
2. PWF zyskuje wielu maintainerów oraz publiczny kanał bezpieczeństwa, **lub**
3. pojawia się niezależna od autora replikacja benchmarków przy n ≥ 30.

Sama nowa wersja upstream ani wzrost liczby gwiazdek **nie są** powodem do ponownego otwarcia.
