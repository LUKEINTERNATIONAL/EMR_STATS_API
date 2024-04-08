#!/bin/bash

# Function to extract database configurations from a specified section
extract_db_config() {
    local section=$1
    local field=$2
    local value=$(awk -v section="$section" -v field="$field" '
        $1 == section ":" {
            in_section = 1
            next
        }
        $1 == "" {
            in_section = 0
        }
        in_section && $1 == field ":" {
            gsub(/^[[:space:]]+|[[:space:]]+$/, "", $0)
            print $2
            exit
        }
    ' /var/www/mlab_api/config/database.yml)
    echo "$value"
}

# Extract database configurations from default section
default_username=$(extract_db_config "default" "username")
default_password=$(extract_db_config "default" "password")
default_host=$(extract_db_config "default" "host")
default_database=$(extract_db_config "default" "database")
default_port=$(extract_db_config "default" "port")

# If the port is blank, set it to 3306
if [ -z "$default_port" ]; then
    default_port=3306
fi

# If the username, password, or database name is blank in default section, try development section
if [ -z "$default_username" ] || [ -z "$default_password" ] || [ -z "$default_database" ]; then
    development_username=$(extract_db_config "development" "username")
    development_password=$(extract_db_config "development" "password")
    development_database=$(extract_db_config "development" "database")
    development_port=$(extract_db_config "development" "port")
    default_username=${development_username:-$default_username}
    default_password=${development_password:-$default_password}
    default_database=${development_database:-$default_database}
    default_port=${development_port:-$default_port}
fi

# Example usage of the extracted configurations
echo "Database configurations:"
echo "Host: $default_host"
echo "Username: $default_username"
echo "Password: $default_password"
echo "Database: $default_database"
echo "Port: $default_port"

# Set up directory for backups
user=$(whoami)
DIR="/home/${user}/remote_backups"

# Create folder if it does not exist
if [ ! -d "$DIR" ]; then
   mkdir "$DIR"
fi

# Log file path
log_file="$DIR/logfile.log"

# Check if any backup file created today exists
today=$(date '+%Y-%m-%d')
backup_files_today=$(find "$DIR" -type f -name "*.sql.gz" -newermt "$today" ! -newermt "$today + 1 day")

if [ -n "$backup_files_today" ]; then
    echo "Backup for today already exists. Skipping backup process."
    echo "$(date '+%Y-%m-%d %H:%M:%S') $default_database - Backup skipped. Backup for today already exists." >> "$log_file"
    exit 0
fi

# Check if both iblis_dump1.sql.gz and iblis_dump2.sql.gz exist
if [ -e "$DIR/iblis_dump1.sql.gz" ] && [ -e "$DIR/iblis_dump2.sql.gz" ]; then
    # Determine which file is the oldest based on modification time
    if [ "$DIR/iblis_dump1.sql.gz" -ot "$DIR/iblis_dump2.sql.gz" ]; then
        oldest_file="$DIR/iblis_dump1.sql.gz"
    else
        oldest_file="$DIR/iblis_dump2.sql.gz"
    fi
    # Extract the file number from the oldest file name
    oldest_file_number=$(echo "$oldest_file" | grep -oE '[0-9]+' | tail -1)
    # Create a new file with the opposite number
    if [ "$oldest_file_number" -eq 1 ]; then
        backup_file="$DIR/iblis_dump2.sql.gz"
    else
        backup_file="$DIR/iblis_dump1.sql.gz"
    fi
else
    # If one of the files doesn't exist, create the opposite file
    if [ ! -e "$DIR/iblis_dump1.sql.gz" ]; then
        backup_file="$DIR/iblis_dump1.sql.gz"
    else
        backup_file="$DIR/iblis_dump2.sql.gz"
    fi
fi

# Create backup and save it in the dir
mysqldump -u"$default_username" -p"$default_password" -h"$default_host" --port="$default_port" --routines "$default_database" | gzip > "$backup_file"

if [ $? -eq 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') $default_database - Backup executed successfully."
    echo "$(date '+%Y-%m-%d %H:%M:%S') $default_database - Backup executed successfully." >> "$log_file"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') $default_database - Backup failed. Check for errors."
    echo "$(date '+%Y-%m-%d %H:%M:%S') $default_database - Backup failed. Check for errors." >> "$log_file"
fi
