#!/bin/bash
VOLUMES_DIR="/var/lib/docker/volumes"

echo "Starting removal of student volumes..."

for volume in "$VOLUMES_DIR"/jupyterhub-user-*; do
    if [ -d "$volume" ]; then
        username=$(basename "$volume" | sed 's/jupyterhub-user-//;s/-my_public//;s/-work//')
        # Check if the username starts with 6 digits (student)
        if [[ $username =~ ^[0-9]{6} ]]; then
            echo "Removing student volume: $(basename "$volume")"
            sudo rm -rf "$volume"
        fi
    fi
done

echo "Removal finished."
