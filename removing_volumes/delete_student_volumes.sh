#!/bin/bash
# Script: delete_student_volumes.sh
# Function: Deletes all volumes belonging to students (identified by a 6-digit login ID).

echo "Starting removal of student volumes (6-digit ID pattern)..."
echo "--- Make sure the servers for these users have been STOPPED! ---"

# Get only the names of Docker volumes
sudo docker volume ls --format "{{.Name}}" | while read VOLUME_NAME; do
    
    # 1. Filter only JupyterHub user volumes
    if [[ $VOLUME_NAME =~ ^jupyterhub-user- ]]; then
        
        # 2. Extract the "clean" username
        USERNAME_PART=${VOLUME_NAME#jupyterhub-user-}
        # Remove suffixes (-work or -my_public)
        CLEAN_USERNAME=${USERNAME_PART%%-work*}
        CLEAN_USERNAME=${CLEAN_USERNAME%%-my_public*}

        # 3. Check if the username starts with 6 digits
        if [[ $CLEAN_USERNAME =~ ^[0-9]{6} ]]; then
            echo "Deleting student volume: $VOLUME_NAME (User: $CLEAN_USERNAME)"
            
            # We use -f (force) for a more reliable deletion after container is stopped
            sudo docker volume rm -f "$VOLUME_NAME"
            
            if [ $? -eq 0 ]; then
                echo "   -> Success."
            else
                echo "   -> Error: Failed to delete $VOLUME_NAME. It might still be in use by an active container."
            fi
        fi
    fi
done

echo "Removal finished."