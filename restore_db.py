import sqlite3
import os
import sys

def list_backups():
    backup_dir = 'database_backups'
    if not os.path.exists(backup_dir):
        print("No backup directory found!")
        return []
    
    backup_files = sorted([f for f in os.listdir(backup_dir) if f.startswith('chat_backup_')])
    if not backup_files:
        print("No backup files found!")
        return []
    
    print("\nAvailable backups:")
    for i, backup in enumerate(backup_files, 1):
        print(f"{i}. {backup}")
    
    return backup_files

def restore_database(backup_file):
    try:
        # Connect to the backup database
        backup_conn = sqlite3.connect(os.path.join('database_backups', backup_file))
        
        # Connect to the main database
        main_conn = sqlite3.connect('chat.db')
        
        # Restore from backup
        backup_conn.backup(main_conn)
        
        # Close connections
        main_conn.close()
        backup_conn.close()
        
        print(f"Database restored successfully from {backup_file}")
        
    except Exception as e:
        print(f"Error restoring database: {e}")

if __name__ == '__main__':
    backup_files = list_backups()
    if not backup_files:
        sys.exit(1)
    
    try:
        choice = int(input("\nEnter the number of the backup to restore: "))
        if 1 <= choice <= len(backup_files):
            restore_database(backup_files[choice-1])
        else:
            print("Invalid choice!")
    except ValueError:
        print("Please enter a valid number!") 