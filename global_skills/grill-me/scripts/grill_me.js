#!/usr/bin/env node

/**
 * 🛸 AGENTS-OS v6.5 — Grill-Me Architectural Pre-Flight Protocol
 */

const cyan = '\x1b[36m';
const yellow = '\x1b[33m';
const green = '\x1b[32m';
const magenta = '\x1b[35m';
const bold = '\x1b[1m';
const reset = '\x1b[0m';

console.log(`${magenta}${bold}====================================================================${reset}`);
console.log(`${cyan}${bold}🛸 [AGENTS-OS v6.5] INICJALIZACJA PROTOKOŁU /grill-me${reset}`);
console.log(`${yellow}Protokół Rygoru Architektonicznego przed Fazą Implementacji (Builder)${reset}`);
console.log(`${magenta}${bold}====================================================================${reset}\n`);

const questions = [
  {
    id: 1,
    topic: "Topologia Maszyn & Dystrybucja Węzłów",
    question: "Na jakich węzłach fizycznych/wirtualnych (Laptop WSL, VPS, Desktop) będzie równolegle wykonywane zadanie i który węzeł ma wyłączność na wdrożenie produkcyjne?",
    prompt: "Zdefiniuj Node ID, ograniczenia sieciowe oraz przypisanie ról w węzłach."
  },
  {
    id: 2,
    topic: "Bezkonfliktowa Synchronizacja & Union Merge",
    question: "Czy wszystkie pliki stanu (.agents/MEMORY.md, .agents/task.md) mają skonfigurowaną regułę 'merge=union' w .gitattributes i czy uwzględniono rebase-safe pull przed sesją?",
    prompt: "Potwierdź strategię rebase oraz format append-only dla logów maszynowych."
  },
  {
    id: 3,
    topic: "Stan Bazy Danych & Wartości Domyślne (Fail-Safe/Fail-Closed)",
    question: "W jaki sposób system zachowa się przy braku połączenia z bazą SQLite/Postgres (czy wdrożono twarde wartości fabryczne - Factory Defaults i podejście Defensive Hybrid)?",
    prompt: "Określ fallbacki dla tabel konfiguracyjnych i politykę kodów błędów HTTP (np. 501 Fail-Closed)."
  },
  {
    id: 4,
    topic: "Potencjalne Kolizje & Krytyczne Przypadki Brzegowe (Edge Cases)",
    question: "Jakie są najgroźniejsze przypadki brzegowe (np. wyczerpanie limitów API, restart demona, ujemny margin, split-brain) i jakie zabezpieczenia (Cooldown, Circuit Breaker) zastosowano?",
    prompt: "Wymień mechanizmy obronne zapobiegające kaskadowym awariom."
  },
  {
    id: 5,
    topic: "Obligatoryjny Zrzut Stanu (State-Dump Mandate R-SYNC-01)",
    question: "W jaki sposób Koordynator i Builder zweryfikują, że przed zakończeniem sesji pamięć operacyjna została zrzucona (state-dump) i zabezpieczona podpisem Handshake?",
    prompt: "Upewnij się, że wygenerowano handshake.json i zaktualizowano MEMORY.md v0.42.1."
  }
];

questions.forEach((q) => {
  console.log(`${green}${bold}[Pytanie ${q.id}] ${q.topic}:${reset}`);
  console.log(`  ❓ ${bold}${q.question}${reset}`);
  console.log(`  💡 ${yellow}Wytyczna:${reset} ${q.prompt}\n`);
});

console.log(`${cyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${reset}`);
console.log(`${yellow}${bold}📋 INSTRUKCJA DLA OPERATORA / KOORDYNATORA:${reset}`);
console.log(`1. Przed przystąpieniem do kodowania wpisz odpowiedzi w ${bold}.agents/MEMORY.md${reset} (sekcja Decisions).`);
console.log(`2. Upewnij się, że zadania są rozpisane w ${bold}task.md${reset} z przypisanymi kryteriami akceptacji.`);
console.log(`3. Po zakończeniu wygeneruj ${bold}_handshake.json${reset} dla roli Auditora.`);
console.log(`${cyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${reset}\n`);
