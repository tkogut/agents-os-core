# Commit Signing — Integrity Control for Swarm State

**Status:** rekomendacja operacyjna (do decyzji użytkownika)
**Kontekst:** przegląd architektoniczny skilla `planning-with-files` (PWF), delta D6
**Zakres:** integralność `.agents/MEMORY.md` i `.agents/task.md` synchronizowanych przez git między maszynami

---

## 1. Dlaczego nie SHA-256 w pliku obok pliku

PWF proponuje attestation: hash SHA-256 pliku planu zapisany w `.plan-attestation`,
a hooki odmawiają działania przy niezgodności. Autorzy PWF sami dokumentują granicę
tego mechanizmu:

> "ordinary local SHA-256 value, not a keyed signature: a process that can replace
> both the plan and the attestation can make new content pass."

Wniosek dla nas: jako kontrola ISO 27001 taki attestation jest **anty-wartościowy**.
Wytwarza audytowalny artefakt sugerujący integralność, której nie zapewnia — czyli
fałszywe zapewnienie w materiale dowodowym audytu. Gorsze niż brak kontroli.

Właściwa kontrola dla stanu trzymanego w gicie to **podpis kryptograficzny commita**.
Jest darmowa, natywna dla nośnika (git), weryfikowalna po stronie serwera (GitHub)
i uznawalna w audycie.

## 2. Dlaczego to NIE jest ustawienie commitowalne do repo

`commit.gpgsign` i `user.signingkey` to konfiguracja **per-maszyna / per-użytkownik**.
Klucz prywatny nigdy nie trafia do repozytorium. Repo może co najwyżej:
- udokumentować wymaganą procedurę (ten plik),
- wymusić skutek po stronie serwera (branch protection → required signatures).

Dlatego niniejsza zmiana **nie ustawia niczego w git config użytkownika**.

## 3. Stan zastany (zweryfikowany 2026-09-16)

| Element | Stan |
|---|---|
| `commit.gpgsign` | nieustawione |
| `gpg.format` | nieustawione |
| `user.signingkey` | nieustawione |
| keyring GPG | **pusty** (brak kluczy tajnych) |
| klucz SSH | obecny: `~/.ssh/tkogut_ssh_key.pub` |
| branch protection na `master` | **brak** (`HTTP 404 Branch not protected`) |
| widoczność repo | **publiczne**, właściciel typu User (nie Organization) |

Konsekwencja: ścieżka GPG wymagałaby wygenerowania nowego klucza. Ścieżka **SSH
signing jest tańsza** — klucz już istnieje i jest już zaufany przez GitHub do pushy.

## 4. Procedura (do wykonania przez użytkownika, per maszyna)

### Wariant zalecany: podpis kluczem SSH

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/tkogut_ssh_key.pub
git config --global commit.gpgsign true
```

Następnie w GitHub: **Settings → SSH and GPG keys → New SSH key → Key type: _Signing Key_**
i wklejenie tego samego klucza publicznego (klucz typu *Authentication* NIE liczy się
do weryfikacji podpisów — musi być dodany osobno jako *Signing Key*).

Weryfikacja lokalna:

```bash
git log --show-signature -1
git verify-commit HEAD
```

### Wariant alternatywny: GPG

```bash
gpg --full-generate-key
gpg --list-secret-keys --keyid-format=long      # odczytaj ID klucza
git config --global user.signingkey <KEY_ID>
git config --global gpg.format openpgp
git config --global commit.gpgsign true
```

Klucz publiczny eksportowany (`gpg --armor --export <KEY_ID>`) i dodany w GitHub jako GPG key.

### Uwaga dla hooków auto-sync

Hooki `SessionEnd` / `Stop` wykonują `git commit` nieinteraktywnie. Przy GPG z
hasłem klucza commit zawiśnie lub cicho padnie (hooki są fail-open — `|| true`).
Wymagany jest agent cache'ujący hasło (`gpg-agent`) albo klucz bez hasła, albo
wariant SSH z `ssh-agent`. **To argument za wariantem SSH.**

## 5. Wymuszenie po stronie serwera — DO DECYZJI UŻYTKOWNIKA

`master` nie ma dziś żadnej ochrony. Włączenie *Require signed commits* jest technicznie
możliwe (repo publiczne → reguły ochrony gałęzi dostępne w planie darmowym).

**Nie wykonano żadnej zmiany w ustawieniach GitHub — zgodnie z zakresem zadania.**

Do rozstrzygnięcia przez użytkownika przed włączeniem:

- [ ] Czy `master` ma dostać branch protection w ogóle (dziś nie ma — to osobne otwarte ryzyko, niezależne od podpisów).
- [ ] Czy włączyć *Require signed commits* — **dopiero po** skonfigurowaniu podpisu na KAŻDEJ maszynie swarmu, inaczej auto-sync z niepodpisanej maszyny zacznie odbijać się przy push.
- [ ] Czy repo ma pozostać **publiczne** — dla firmowego tooling repo pod ISO 27001 to samodzielna kwestia do rozstrzygnięcia, tu tylko odnotowana.
- [ ] Czy egzekwować podpisy także dla commitów generowanych przez hooki (`chore(sync): ...`) — jeśli tak, konfiguracja agenta klucza na każdej maszynie jest warunkiem koniecznym.

Polecenie referencyjne (NIE uruchamiane automatycznie):

```bash
gh api -X PUT repos/tkogut/agents-os-core/branches/master/protection/required_signatures
```

## 6. Kryterium zamknięcia

Kontrola D6 uznawana jest za wdrożoną, gdy:
1. każda maszyna swarmu podpisuje commity (`git verify-commit HEAD` przechodzi),
2. `master` wymaga podpisanych commitów po stronie GitHub,
3. procedura jest odnotowana w SDLC (zrobione — patrz `SDLC.md`, Hard Rules).

Do tego czasu **nie należy** twierdzić w materiale audytowym, że stan swarmu ma
kontrolę integralności.
