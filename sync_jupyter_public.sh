#!/bin/bash

SOURCE_BASE="/var/lib/docker/volumes/jupyterhub-user-"
DEST_BASE="/var/lib/docker/volumes/jupyterhub-public/_data"

# Function to synchronize user data
sync_user_data() {
    local username="$1"
    local source_path="${SOURCE_BASE}${username}-my_public/_data/"
    local dest_path="${DEST_BASE}/${username}/"

    if [ -d "$source_path" ]; then
        mkdir -p "$dest_path"
        rsync -av --delete "$source_path" "$dest_path" > /dev/null 2>&1
        echo "[$(date)] Synchronized user data: $username"
    else
        echo "[$(date)] No _data folder found for user: $username"
    fi
}

# Main monitoring loop
while true; do
    # Find all user folders
    find "/var/lib/docker/volumes/" -maxdepth 1 -type d -name "jupyterhub-user-*-my_public" | while read -r user_folder; do
        username=$(basename "$user_folder" | sed 's/jupyterhub-user-\(.*\)-my_public/\1/')
        sync_user_data "$username"

        # Run inotifywait in the background for each folder
        if ! pgrep -f "inotifywait.*${user_folder}/_data" > /dev/null; then
            inotifywait -r -m -e modify,create,delete --format "%w%f" "${user_folder}/_data/" | while read -r changed_file; do
                sync_user_data "$username"
            done &
        fi
    done
    sleep 5   # Wait 5 seconds before the next scan
done
