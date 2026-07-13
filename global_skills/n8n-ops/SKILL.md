---
name: n8n-ops
description: Operational guide for managing n8n workflows via docker exec/cp on Hostinger VPS (export, import, debug, multi-instance isolation with Traefik).
trigger_words: [n8n, workflow, n8n-import, n8n-export, docker exec n8n, n8n workflow json, n8n instancja, n8n VPS, n8n ops, importuj workflow, eksportuj workflow]
---

# n8n-ops — Operational Skill v1.1

## 0. Pre-Flight Checklist

Before any n8n operation:
1. Identify target instance: **g7tq** vs **pkogut**
2. Load SSH socket from `vps-ops` skill pattern (Note: the `n8n_helper.py` script attempts to automatically detect `SSH_AUTH_SOCK` from `/tmp/` processes).
3. Confirm container name (see §6)

---

## 1. Automated Operations with `n8n_helper.py` (Recommended)

W katalogu `global_skills/n8n-ops/scripts/` (lub w folderze `.agents/skills/n8n-ops/scripts/` lokalnego projektu) znajduje się skrypt pomocniczy automatyzujący całą komunikację z VPS.

### 1.1 List instances and status
```bash
python3 scripts/n8n_helper.py list
```

### 1.2 Import workflow
```bash
python3 scripts/n8n_helper.py import --instance g7tq --file path/to/local/workflow.json
```
*(Automatycznie dodaje tymczasowe ID, przesyła plik, kopiuje do kontenera, importuje i sprząta).*

### 1.3 Export workflow to local file
```bash
python3 scripts/n8n_helper.py export --instance g7tq --id AUssdU21qSE04Wfo --output local_workflow.json
```

### 1.4 Backup all workflows from instance
```bash
python3 scripts/n8n_helper.py backup --instance g7tq --dir ./n8n_backups
```

---

## 2. Manual Export Workflow from n8n (Fallback)

```bash
# Pattern — export workflow by ID manually
SSH_AUTH_SOCK=<socket> ssh root@srv1490214.hstgr.cloud \
  "docker exec -i <container> n8n export:workflow --id=<workflow_id>"
```

> **Use case:** backup, inspect existing workflow JSON before editing manually.

---

## 3. Manual Import Workflow — Full Procedure

### 3.1 Create JSON on VPS host (NOT locally)

```bash
SSH_AUTH_SOCK=<socket> ssh root@srv1490214.hstgr.cloud "cat << 'EOF' > /tmp/workflow.json
{
  <your workflow JSON here>
}
EOF"
```

### 3.2 Copy to container

```bash
SSH_AUTH_SOCK=<socket> ssh root@srv1490214.hstgr.cloud \
  "docker cp /tmp/workflow.json <container>:/tmp/workflow.json"
```

### 3.3 Import

```bash
SSH_AUTH_SOCK=<socket> ssh root@srv1490214.hstgr.cloud \
  "docker exec -i <container> n8n import:workflow --input=/tmp/workflow.json"
```

### 3.4 Verify import

```bash
SSH_AUTH_SOCK=<socket> ssh root@srv1490214.hstgr.cloud \
  "docker exec -i <container> n8n export:workflow --id=<workflow_id>"
```

### 3.5 Cleanup

```bash
SSH_AUTH_SOCK=<socket> ssh root@srv1490214.hstgr.cloud \
  "rm /tmp/workflow.json && docker exec -i <container> rm /tmp/workflow.json"
```

---

## 4. Workflow JSON Structure — Required Fields

```json
{
  "id": "TEST123456789ABC",
  "name": "My Workflow",
  "nodes": [],
  "connections": {},
  "settings": {
    "executionOrder": "v1"
  },
  "meta": {
    "instanceId": ""
  }
}
```

### Node schema (every node MUST have all fields):

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Node Display Name",
  "type": "n8n-nodes-base.manualTrigger",
  "typeVersion": 1,
  "position": [250, 300],
  "parameters": {}
}
```

---

## 5. Known Node Types — Quick Reference

| Node | type | typeVersion | Notes |
|------|------|-------------|-------|
| Manual Trigger | n8n-nodes-base.manualTrigger | 1 | No parameters needed |
| Schedule Trigger | n8n-nodes-base.scheduleTrigger | 1.3 | See §5.1 |
| Google Drive | n8n-nodes-base.googleDrive | 3 | Requires credentials |
| Google Sheets | n8n-nodes-base.googleSheets | 4.7 | Requires credentials |
| Extract From File | n8n-nodes-base.extractFromFile | 1.1 | |
| Merge | n8n-nodes-base.merge | 3.2 | |
| Switch | n8n-nodes-base.switch | 3.4 | |

### 5.1 Schedule Trigger parameters example

```json
{
  "parameters": {
    "rule": {
      "interval": [
        { "triggerAtHour": 9 }
      ]
    }
  }
}
```

---

## 6. Error Lookup Table

| Error | Root Cause | Fix |
|-------|-----------|-----|
| An input file or directory with --input must be provided | Missing --input= flag | Always use --input=/tmp/file.json |
| ENOENT: no such file or directory | File on host, not inside container | Run docker cp BEFORE docker exec |
| SQLITE_CONSTRAINT: NOT NULL constraint failed: workflow_entity.id | JSON missing root-level id field | Add "id": "ALPHANUMERIC_STRING" to workflow JSON root |

---

## 7. Multi-Instance Architecture (Hostinger VPS)

**Host:** srv1490214.hstgr.cloud

| Instance | Compose Dir | Container | Domain |
|----------|-------------|-----------|--------|
| g7tq | /docker/n8n-g7tq | n8n-g7tq-n8n-1 | n8n-g7tq.srv1490214.hstgr.cloud |
| pkogut | /docker/n8n-pkogut | n8n-pkogut-n8n-1 | n8n-pkogut.srv1490214.hstgr.cloud |

### 7.1 docker-compose.yml — template for new isolated instance

```yaml
# Zamien <nazwa> na unikalny identyfikator instancji (np. "jkowalski")
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    restart: unless-stopped
    volumes:
      - n8n_data_<nazwa>:/home/node/.n8n
    networks:
      - traefik-proxy
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.<nazwa>.rule=Host(`<nazwa>.srv1490214.hstgr.cloud`)"
      - "traefik.http.routers.<nazwa>.entrypoints=websecure"
      - "traefik.http.routers.<nazwa>.tls.certresolver=letsencrypt"
      - "traefik.http.services.<nazwa>.loadbalancer.server.port=5678"

networks:
  traefik-proxy:
    external: true

volumes:
  n8n_data_<nazwa>:
```

---

## 8. Free Tier Constraint

> **n8n Free = 1 user per instance.**
> Multiple users → deploy separate isolated instances (see §7).

---

## 9. Agent Execution Protocol

When user requests n8n work, follow this sequence **strictly**:

```
1. ASK    → which instance? (g7tq / pkogut)
2. EXEC   → Use scripts/n8n_helper.py tool for automated import/export/list
3. VERIFY → Check status with python3 scripts/n8n_helper.py list
```

---

## 10. Connections Format Reference

```json
"connections": {
  "Source Node Name": {
    "main": [
      [
        {
          "node": "Target Node Name",
          "type": "main",
          "index": 0
        }
      ]
    ]
  }
}
```

> main[0] = first output branch. Multi-branch nodes (Switch) use main[0], main[1], etc.
