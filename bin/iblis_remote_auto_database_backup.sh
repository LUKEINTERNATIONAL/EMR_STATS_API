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


# Create backup file with current date
backup_file="$DIR/$(date '+%A')_$default_database.sql.gz"

# Check if there are already 2 backup files, delete the oldest one if yes
num_backups=$(ls -1 "$DIR"/*.sql.gz 2>/dev/null | wc -l)
if [ "$num_backups" -ge 2 ]; then
    oldest_backup=$(ls -t "$DIR"/*.sql.gz | tail -1)
    rm "$oldest_backup"
fi

# Create backup and save it in the dir
mysqldump -u"$default_username" -p"$default_password" -h"$default_host" --port="$default_port" --routines "$default_database" | gzip > "$backup_file"

if [ $? -eq 0 ]; then
    echo "executed successfully."
else
    echo "Check for errors."
fi
