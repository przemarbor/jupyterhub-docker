#!/bin/bash
# Script: delete_all_user_volumes.sh
# Function: Deletes ALL volumes created for JupyterHub users.

echo "!!! WARNING: This script will delete ALL working data of all users !!!"
echo "--- Make sure ALL user servers have been STOPPED! ---"
echo "------------------------------------------------------------------------"

read -p "Are you sure you want to delete ALL user volumes? (type YES to continue): " CONFIRMATION

if [ "$CONFIRMATION" != "YES" ]; then
    echo "Deletion cancelled."
    exit 0
fi

echo "Starting deletion of ALL user volumes..."

# Filter only user volumes (starting with jupyterhub-user-)
# We use --format to get only the names.
USER_VOLUMES=$(sudo docker volume ls --format "{{.Name}}" | grep '^jupyterhub-user-')

if [ -z "$USER_VOLUMES" ]; then
    echo "No user volumes found to delete."
    exit 0
fi

echo "$USER_VOLUMES" | while read VOLUME_NAME; do
    echo "Deleting volume: $VOLUME_NAME"
    
    # We use -f (force)
    sudo docker volume rm -f "$VOLUME_NAME"
    
    if [ $? -eq 0 ]; then
        echo "   -> Success."
    else
        echo "   -> Error: Failed to delete $VOLUME_NAME."
    fi
done

echo "Finished deleting ALL user volumes."