# Raport Refaktoryzacji AGENTS-OS do wersji v4.2.1 Swarm Edition

## 1. Cel i zakres refaktoryzacji
Niniejszy raport przedstawia strategię i konkretne kroki niezbędne do zmigrowania środowiska AGENTS-OS z przestarzałej wersji korzystającej z `gemini-cli` i dystrybucji `snap` na natywny ekosystem **Antigravity CLI** wprowadzony w wersji v4.2.1. Decyzja ta podyktowana jest m.in. wygasaniem wsparcia dla starych tokenów deweloperskich (18 czerwca 2026 r.).

## 2. Identyfikacja Długu Technologicznego (Legacy Code)
Analiza repozytorium wykazała, że obecny instalator (`INSTALL.sh`) oraz powiązane skrypty posiadały kilka krytycznych wad:
* **Zależność od Snap:** Mocne sprzężenie ze środowiskiem snap uniemożliwiało instalację systemu na macOS oraz w czystych kontenerach (np. Docker, Devcontainers) i powodowało problemy z systemem dowiązań symbolicznych (konieczność omijania przez tzw. "Snap Sandbox Guard").
* **Przestarzałe narzędzia CLI:** Wykorzystywanie `gemini-cli`, które wg oficjalnego changelogu i dokumentów Google zostało zastąpione przez wbudowane środowisko w Antigravity.
* **Manualne zarządzanie skilami:** Kopiowanie skilli z pominięciem natywnych mechanizmów, co narusza zasady *Konstytucji AGENTS-OS v4.0*.

## 3. Zrefaktoryzowany Skrypt Inicjalizujący (`INSTALL.sh`)
Skrypt instalacyjny wymaga głębokiej refaktoryzacji, aby dostosować go do wymogów architektonicznych v4.2.1. Należy wyeliminować dług technologiczny i oprzeć się na uniwersalnych menedżerach pakietów (apt/brew) oraz natywnym Antigravity CLI. 

*Uwaga: Zgodnie z architekturą roju, bezpośrednia implementacja i kod skryptu `INSTALL.sh` zostaną wygenerowane i wdrożone autonomicznie przez agenta Antigravity CLI w ramach wewnętrznej pętli wykonawczej.*

## 4. Dalsze Kroki i Rekomendacje dla Architekta
Po udanym wdrożeniu nowego instalatora przez Agenta, proces refaktoryzacji w The Swarm Triad powinien objąć:
1.  **Weryfikację Silnika `bootstrap.py`:** Należy upewnić się, że główny skrypt Pythona inicjalizujący projekty poprawnie interpretuje nowe komendy Antigravity (np. wymuszenie trybu autonomicznego przez `/goal`).
2.  **Integrację MCP (`mcp_config.json`):** Sprawdzenie, czy serwer ustrukturyzowanej dokumentacji Playwright (`antigravity-docs`) wstaje bezbłędnie na systemach macOS bez konieczności rekonfiguracji środowiska graficznego.
3.  **Audyt Bezpieczeństwa:** Ostateczne testy bezpieczeństwa modułu `os-add-skill` mające na celu potwierdzenie załatania podatności na ataki typu *Path Traversal*.
