# /handshake — Generate Builder Handshake JSON
#
# Usage: /handshake
# Signals implementation complete. Triggers Auditor QA Gate.

Generate a Swarm Triad builder handshake JSON for this session.

Steps:
1. Detect current branch:
   ```bash
   BRANCH=$(git rev-parse --abbrev-ref HEAD)
   ```
2. Detect last commit message:
   ```bash
   LAST_COMMIT=$(git log -1 --pretty=%s)
   ```
3. Ask me: "Brief task description for the handshake? (1 sentence)"
4. Generate handshake:
   ```bash
   python3 scripts/generate-handshake.py \
     --role builder \
     --task "<task description from step 3>" \
     --branch "$BRANCH" \
     --status complete
   ```
5. Show me the path of the generated handshake JSON file.
6. Remind me: "Handshake generated. Coordinator/Auditor can now begin QA Gate (SDLC Phase 5)."

Output: `.agents/swarm/<session-id>_builder_handshake.json`
