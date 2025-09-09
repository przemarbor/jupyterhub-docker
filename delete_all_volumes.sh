#!/bin/bash

# Configuration
VOLUMES_DIR="/var/lib/docker/volumes"
VOLUMES_TO_REMOVE=("$VOLUMES_DIR"/jupyterhub-user-* "$VOLUMES_DIR"/jupyterhub-public)

echo "Starting removal of all Jupyter volumes..."

for volume in "${VOLUMES_TO_REMOVE[@]}"; do
    if [ -d "$volume" ]; then
        echo "Removing volume: $(basename "$volume")"
        sudo rm -rf "$volume"
    fi
done

echo "Removal finished."
