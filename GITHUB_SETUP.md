# GitHub Setup Guide

This guide will help you push your ChatBoard application to GitHub.

## Prerequisites

1. A GitHub account (sign up at github.com if you don't have one)
2. Git installed on your computer
3. Your project files

## Step 1: Initialize Git Repository

1. Open terminal/command prompt
2. Navigate to your project directory:
   ```bash
   cd /path/to/your/chatboard
   ```
3. Initialize Git repository:
   ```bash
   git init
   ```

## Step 2: Create GitHub Repository

1. Log in to your GitHub account
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Fill in the repository details:
   - Repository name: `chatboard` (or your preferred name)
   - Description: "A simple chat application with user authentication and real-time messaging"
   - Choose "Public" or "Private" as per your preference
   - Do NOT initialize with README (we already have one)
5. Click "Create repository"

## Step 3: Add Remote Repository

1. Copy the repository URL from GitHub
2. Add the remote repository:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/chatboard.git
   ```
   (Replace YOUR_USERNAME with your GitHub username)

## Step 4: Stage and Commit Files

1. Stage all files:
   ```bash
   git add .
   ```
2. Commit the files:
   ```bash
   git commit -m "Initial commit: ChatBoard application with user authentication and real-time messaging"
   ```

## Step 5: Push to GitHub

1. Push your code to GitHub:
   ```bash
   git push -u origin main
   ```
   (If you get an error about the branch name, try `master` instead of `main`)

## Step 6: Verify Upload

1. Go to your GitHub repository
2. Verify that all files are uploaded correctly
3. Check that sensitive files (like database files) are not included

## Important Notes

1. **Never commit sensitive information**:

   - Database files
   - API keys
   - Passwords
   - Personal information

2. **Branch Management**:

   - Create feature branches for new features
   - Use pull requests for code review
   - Keep main branch stable

3. **Commit Messages**:
   - Be descriptive
   - Follow conventional commit format
   - Reference issues if applicable

## Common Git Commands

```bash
# Create and switch to a new branch
git checkout -b feature-name

# Switch branches
git checkout branch-name

# Pull latest changes
git pull origin main

# Push changes to branch
git push origin branch-name

# View status
git status

# View commit history
git log
```

## Troubleshooting

1. **Authentication Issues**:

   - Use SSH keys for better security
   - Configure Git credentials
   - Use personal access tokens

2. **Push Rejected**:

   - Pull latest changes first
   - Resolve conflicts
   - Try force push (use with caution)

3. **Large Files**:
   - Use Git LFS for large files
   - Check file size limits
   - Remove large files from history if needed

## Best Practices

1. **Regular Commits**:

   - Commit often
   - Keep commits focused
   - Write clear commit messages

2. **Branch Strategy**:

   - Use feature branches
   - Keep main branch clean
   - Delete merged branches

3. **Code Review**:

   - Use pull requests
   - Request reviews
   - Address feedback

4. **Security**:
   - Review .gitignore
   - Check for sensitive data
   - Use branch protection
