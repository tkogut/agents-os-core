# /handshake — Generate Builder Handshake JSON
#
# Usage: /handshake
# Signals implementation complete. Triggers Auditor QA Gate (SDLC Phase 4).

Generate a Swarm Triad builder handshake JSON for this session.

Steps:
1. Generate a session UUID:
   ```bash
   SESSION_ID=$(python3 -c "import uuid; print(uuid.uuid4())")
   echo "Session ID: $SESSION_ID"
   ```
2. List modified files:
   ```bash
   git diff --name-only HEAD~1 HEAD 2>/dev/null || git diff --cached --name-only
   ```
3. Ask me: "Brief description of completed task (for notes field)?"
4. Run:
   ```bash
   python3 scripts/generate-handshake.py \
     --role builder \
     --conversation-id "$SESSION_ID" \
     --status SUCCESS \
     --files "<comma-separated list from step 2>" \
     --notes "<task description from step 3>"
   ```
5. Show the path and content summary of the generated handshake JSON.
6. Print: "✅ Handshake registered at .agents/swarm/${SESSION_ID}_builder_handshake.json"
7. Remind: "Coordinator/Auditor can now begin QA Gate (SDLC Phase 5)."

Output: `.agents/swarm/<session-id>_builder_handshake.json`
