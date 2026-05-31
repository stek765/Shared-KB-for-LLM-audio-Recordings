#!/usr/bin/env bash
# Auto-sync KB con GitHub — pull + commit + push
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"

TIMESTAMP="$(date '+%Y-%m-%d %H:%M')"
LOG="$REPO_DIR/.git/sync.log"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

# --- PULL ---
log "Pull..."
git fetch origin main 2>>"$LOG"

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" != "$REMOTE" ]; then
    git merge --ff-only origin/main >>"$LOG" 2>&1 && log "Aggiornato da remoto." || {
        log "Merge non fast-forward, merge manuale richiesto."
        exit 1
    }
fi

# --- COMMIT se ci sono modifiche ---
if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
    git add -A

    # Messaggio pertinente: file modificati
    CHANGED=$(git diff --cached --name-only | head -5 | sed 's|.*/||' | tr '\n' ', ' | sed 's/,$//')
    [ -z "$CHANGED" ] && CHANGED="aggiornamenti vari"

    MSG="[$TIMESTAMP] $CHANGED"
    git commit -m "$MSG" >>"$LOG" 2>&1
    log "Commit: $MSG"
else
    log "Nessuna modifica locale."
fi

# --- PUSH ---
if [ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main 2>/dev/null || echo '')" ]; then
    git push origin main >>"$LOG" 2>&1 && log "Push completato." || log "Push fallito."
else
    log "Già sincronizzato."
fi

# --- REINDEX ---
log "Reindex KB..."
"$REPO_DIR/.venv/bin/python" "$REPO_DIR/search.py" index >>"$LOG" 2>&1 && log "Reindex completato." || log "Reindex fallito (ignorato)."
