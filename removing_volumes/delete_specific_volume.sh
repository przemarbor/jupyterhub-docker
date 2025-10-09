#!/bin/bash
# Script: delete_specific_volume.sh
# Function: Lists user volumes and deletes the selected volume.

echo "--- Available JupyterHub User Volumes ---"

# Filter only user volumes (starting with jupyterhub-user-)
USER_VOLUMES=$(sudo docker volume ls --format "{{.Name}}" | grep '^jupyterhub-user-')

if [ -z "$USER_VOLUMES" ]; then
    echo "No user volumes found."
    exit 0
fi

echo "$USER_VOLUMES"
echo "------------------------------------------------"

read -p "Enter the EXACT volume name to delete (e.g., jupyterhub-user-123456-work): " VOLUME_TO_DELETE

if [ -z "$VOLUME_TO_DELETE" ]; then
    echo "Cancelled. No volume name provided."
    exit 0
fi

if echo "$USER_VOLUMES" | grep -q "^$VOLUME_TO_DELETE$"; then
    echo "Confirm deletion of volume: $VOLUME_TO_DELETE"
    read -p "Are you sure you want to delete this volume? (y/N): " CONFIRMATION

    if [[ "$CONFIRMATION" =~ ^[Yy]$ ]]; then
        echo "Deleting $VOLUME_TO_DELETE..."
        # Using -f (force) in case the container was deleted previously but Docker still holds an old entry.
        sudo docker volume rm -f "$VOLUME_TO_DELETE"
        
        if [ $? -eq 0 ]; then
            echo "Success: Volume $VOLUME_TO_DELETE has been successfully deleted."
        else
            echo "Error: Failed to delete volume $VOLUME_TO_DELETE. Make sure the user's server is STOPPED."
        fi
    else
        echo "Deletion cancelled."
    fi
else
    echo "Error: Volume named '$VOLUME_TO_DELETE' is not a user volume or does not exist."
fi