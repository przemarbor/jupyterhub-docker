# Konfiguracja
VOLUMES_DIR="/var/lib/docker/volumes"
BACKUP_DIR="/home/pawwlad/project/jhInDocker/backups" # Default backup folder
DATE=$(date +%F)
TARGET_DIR="$BACKUP_DIR/$DATE"

# Tworzenie katalogu backupowego
mkdir -p "$TARGET_DIR"

# Funkcja sprawdzająca, czy nazwa należy do wykładowcy (nie ma 6 cyfr na początku)
is_teacher() {
    local username=$(basename "$1" | sed 's/jupyterhub-user-//;s/-my_public//;s/-work//')
    [[ ! $username =~ ^[0-9]{6} ]]
}

# Backup woluminów wykładowców (my_public i work)
for volume in "$VOLUMES_DIR"/jupyterhub-user-*; do
    if [ -d "$volume" ] && is_teacher "$volume"; then
        volume_type=$(basename "$volume" | awk -F'-' '{print $NF}')  # my_public or work
        echo "Copying TEACHER volume: $(basename "$volume") (type: $volume_type)"
        cp -a "$volume" "$TARGET_DIR/"
    fi
done

# Backup woluminu publicznego (dla wszystkich)
if [ -d "$VOLUMES_DIR/jupyterhub-public" ]; then
    echo "Copying public volume"
    cp -a "$VOLUMES_DIR/jupyterhub-public" "$TARGET_DIR/"
fi

# Authorisations
setfacl -R -m u:pawwlad:r-x "$TARGET_DIR" # Default user

# Cleaning
backup_count=$(ls -1 "$BACKUP_DIR" | wc -l)
if [ "$backup_count" -gt 4 ]; then
    echo "Backup count: $backup_count. Deleting oldest backups..."
    ls -1t "$BACKUP_DIR" | tail -n +5 | while read old_backup; do
        rm -rf "$BACKUP_DIR/$old_backup"
        echo "Deleted: $old_backup"
    done
fi

# Podsumowanie
echo "Backup finished. Saved to: $TARGET_DIR"
ls -lh "$TARGET_DIR"
