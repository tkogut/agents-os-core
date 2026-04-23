---
name: browser-connectivity
description: Globalny systemowy skill dla browser-connectivity (CDP Bridge) w AGENTS-OS v3.2.
---

# 🌐 Browser Connectivity (CDP Bridge)

🎯 **Purpose**
Zarządzanie połączeniem przeglądarki w środowisku WSL2 przy użyciu mostka CDP (Chrome DevTools Protocol). Skill ten wymusza połączenie z instancją Chrome na Windows zamiast prób uruchamiania lokalnego.

🛠️ **Implementation Logic**

Agent używa \`browserType.connectOverCDP\` zamiast \`browser.launch()\`.

1. **Endpoint**: \`http://127.0.0.1:9222\` (Zmapowany tunel w WSL).
2. **Profil**: Używaj profilu \`roostertk\`.

🚀 **Verification Workflow (Check_Bridge_Health)**
1. **Wykrywanie IP**: \`ip route show | grep default | awk '{print $3}'\`.
2. **Audit Mostka**: Sprawdź czy skrypt \`wsl_bridge_universal.py\` lub \`start_tunnel.py\` jest aktywny w procesach.
3. **Ping**: \`curl -I http://127.0.0.1:9222/json/version\`.

⚠️ **Error Recovery**
- Jeśli mostek leży: Wykonaj \`python3 execution/start_tunnel.py\`.
- Jeśli port 9223 zablokowany: Poproś użytkownika o \`netsh interface portproxy reset\` na Windows.

Standard AntiGravity v3.2 Swarm | Browser Bridge Active.
