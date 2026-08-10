#!/bin/bash

# This script installs the 'os-init-zed' function for initializing Zed projects.

BASHRC_D_DIR="$HOME/.bashrc.d"
ANTIGRAVITY_FILE="$BASHRC_D_DIR/antigravity"
AGENTS_CORE_PATH="$HOME/agents-os-core" # Assuming a standard location

# Ensure the target directory exists
mkdir -p "$BASHRC_D_DIR"

# The function definition using a heredoc for clarity
FUNCTION_DEFINITION=$(cat <<'EOF'

# Initializes a new project workspace for the Zed editor
os-init-zed() {
    if [ -z "$1" ]; then
        echo "Usage: os-init-zed <project_name>"
        return 1
    fi
    python3 ~/agents-os-core/execution/bootstrap_zed.py "$1"
}
EOF
)

# Check if the function already exists to prevent duplicates
if ! grep -q "os-init-zed()" "$ANTIGRAVITY_FILE" 2>/dev/null; then
    echo "Appending 'os-init-zed' function to $ANTIGRAVITY_FILE..."
    # Append the function definition to the file
    echo "$FUNCTION_DEFINITION" >> "$ANTIGRAVITY_FILE"
    echo "Installation complete."
    echo "Please run 'source ~/.bashrc' or restart your shell to use the new command."
else
    echo "'os-init-zed' function already exists in $ANTIGRAVITY_FILE. No action taken."
fi
