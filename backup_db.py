import sqlite3
import shutil
import os
from datetime import datetime

def backup_database():
    # Create backup directory if it doesn't exist
    backup_dir = 'database_backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f'chat_backup_{timestamp}.db')
    
    # Create backup
    try:
        # Connect to the database
        conn = sqlite3.connect('chat.db')
        
        # Create a backup
        backup_conn = sqlite3.connect(backup_file)
        conn.backup(backup_conn)
        
        # Close connections
        backup_conn.close()
        conn.close()
        
        print(f"Backup created successfully: {backup_file}")
        
        # Keep only the last 5 backups
        backup_files = sorted([f for f in os.listdir(backup_dir) if f.startswith('chat_backup_')])
        if len(backup_files) > 5:
            for old_backup in backup_files[:-5]:
                os.remove(os.path.join(backup_dir, old_backup))
                print(f"Removed old backup: {old_backup}")
                
    except Exception as e:
        print(f"Error creating backup: {e}")

if __name__ == '__main__':
    backup_database() 