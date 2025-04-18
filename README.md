# ChatBoard - Simple Chat Application

A simple web-based chat application with user authentication and real-time messaging capabilities.

## Features

- User authentication with hardcoded credentials
- Real-time messaging
- Support for text messages, images, and emojis
- Simple and intuitive interface
- Database backup and restore functionality

## Setup Instructions

1. Make sure you have Python 3.7+ installed on your system.

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python app.py
```

5. Open your web browser and navigate to:

```
http://localhost:5000
```

## Default User Credentials

The following users are pre-configured in the system:

- Username: `admin`, Password: `password123`
- Username: `user1`, Password: `password123`
- Username: `user2`, Password: `password123`

## Features Usage

- **Text Messages**: Type your message in the input box and press Enter or click Send
- **Images**: Click the 📷 button to upload and send images
- **Emojis**: Click the emoji picker to add emojis to your messages

## Database Backup and Restore

### Creating Backups

1. Run the backup script:

```bash
python backup_db.py
```

This will:

- Create a backup in the `database_backups` directory
- Name the backup file with a timestamp (e.g., `chat_backup_20240315_143022.db`)
- Automatically keep only the last 5 backups

### Restoring from Backup

1. Run the restore script:

```bash
python restore_db.py
```

2. The script will show a list of available backups
3. Enter the number of the backup you want to restore

### Automated Backups

#### Linux/Mac

Add this to your crontab to create daily backups at midnight:

```bash
0 0 * * * cd /path/to/your/app && python backup_db.py
```

#### Windows

Create a scheduled task that runs:

```bash
python C:\path\to\your\app\backup_db.py
```

## Migrating to a New Server

### Step 1: Backup on Old Server

1. Stop the chat application
2. Create a final backup:

```bash
python backup_db.py
```

3. Copy the following to your new server:
   - The entire application directory
   - The latest backup file from `database_backups` directory

### Step 2: Setup on New Server

1. Install Python 3.7+ if not already installed
2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Restore the database:

```bash
python restore_db.py
```

5. Start the application:

```bash
python app.py
```

### Step 3: Verify Migration

1. Access the application on the new server
2. Verify that:
   - All users can log in
   - Previous messages are visible
   - New messages can be sent
   - Image uploads work correctly

## Security Note

This is a simple demonstration application. In a production environment, you should:

- Use proper password hashing
- Implement proper session management
- Use HTTPS
- Store credentials in a secure database
- Implement proper input validation and sanitization
- Store backups in a secure location
- Consider encrypting backup files

## Project Structure

```
.
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── backup_db.py       # Database backup script
├── restore_db.py      # Database restore script
├── static/            # Static files (CSS, JS, images)
│   └── uploads/       # Directory for uploaded images
├── database_backups/  # Directory for database backups
└── templates/         # HTML templates
    ├── login.html     # Login page
    └── chat.html      # Chat interface
```
