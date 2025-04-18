# Deployment Guide - PythonAnywhere

This guide will help you deploy your ChatBoard application on PythonAnywhere.

## Prerequisites

1. A PythonAnywhere account (sign up at pythonanywhere.com)
2. Your application files
3. A web browser

## Step 1: Upload Your Files

1. Log in to your PythonAnywhere account
2. Go to the "Files" tab
3. Create a new directory for your project (e.g., `chatboard`)
4. Upload all your project files:
   - app.py
   - requirements.txt
   - templates/
   - static/
   - backup_db.py
   - restore_db.py

## Step 2: Set Up Virtual Environment

1. Open a Bash console from the PythonAnywhere dashboard
2. Navigate to your project directory:
   ```bash
   cd chatboard
   ```
3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Step 3: Set Up Web App

1. Go to the "Web" tab in PythonAnywhere
2. Click "Add a new web app"
3. Choose "Manual Configuration"
4. Select Python version (3.7 or higher)
5. Click "Next"

## Step 4: Configure Web App

1. In the Web tab, find the "Code" section
2. Set the following:

   - Source code: `/home/yourusername/chatboard`
   - Working directory: `/home/yourusername/chatboard`
   - Virtualenv: `/home/yourusername/chatboard/venv`

3. In the "WSGI configuration file" section:

   - Click on the file link
   - Replace the content with:

   ```python
   import sys
   path = '/home/yourusername/chatboard'
   if path not in sys.path:
       sys.path.append(path)

   from app import app as application
   ```

## Step 5: Set Up Database

1. In the Web tab, find the "Static files" section
2. Add the following mappings:

   - URL: `/static`
   - Directory: `/home/yourusername/chatboard/static`

3. Create necessary directories:
   ```bash
   mkdir -p static/uploads
   mkdir -p database_backups
   ```

## Step 6: Configure Domain

1. In the Web tab, find the "Domain" section
2. You can use the default PythonAnywhere domain or set up a custom domain
3. For custom domain, you'll need to:
   - Purchase a domain
   - Set up DNS records
   - Configure SSL

## Step 7: Start the Application

1. In the Web tab, click "Reload" to start your application
2. Your app should now be running at:
   - Free account: `yourusername.pythonanywhere.com`
   - Paid account: Your custom domain

## Step 8: Set Up Automated Backups

1. Go to the "Tasks" tab
2. Add a new scheduled task:
   ```bash
   cd /home/yourusername/chatboard && source venv/bin/activate && python backup_db.py
   ```
3. Set the schedule (e.g., daily at midnight)

## Troubleshooting

1. **Application Not Starting**

   - Check the error log in the Web tab
   - Verify all dependencies are installed
   - Ensure file permissions are correct

2. **Database Issues**

   - Check if the database file exists
   - Verify file permissions
   - Try restoring from backup if needed

3. **Static Files Not Loading**
   - Verify static file mappings
   - Check file permissions
   - Clear browser cache

## Maintenance

1. **Regular Backups**

   - Monitor backup tasks
   - Verify backup files are created
   - Test restore functionality periodically

2. **Updates**

   - Test updates in a separate environment
   - Backup before updating
   - Deploy updates during low-traffic periods

3. **Monitoring**
   - Check error logs regularly
   - Monitor disk space
   - Watch for unusual activity

## Security Considerations

1. **SSL**

   - Enable SSL for your domain
   - Use HTTPS for all connections

2. **File Permissions**

   - Set appropriate file permissions
   - Restrict access to sensitive files

3. **Backups**
   - Store backups securely
   - Consider encrypting backup files

## Scaling

If your application grows:

1. Upgrade to a paid PythonAnywhere account
2. Consider moving to a more scalable platform
3. Implement proper database management
4. Add load balancing if needed
