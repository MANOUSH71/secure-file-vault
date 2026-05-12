#!/usr/bin/env python3
"""
Database Models - SQLite Database for User and File Management
"""

import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash
from pathlib import Path


class Database:
    def __init__(self, db_path='vault.db'):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table (enhanced)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT,
                preferred_language TEXT DEFAULT 'en',
                is_active INTEGER DEFAULT 1,
                require_2fa INTEGER DEFAULT 0,
                totp_secret TEXT,
                last_login TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Files table (enhanced with expiry, folder, tags)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                file_id TEXT UNIQUE NOT NULL,
                original_name TEXT NOT NULL,
                encrypted_name TEXT NOT NULL,
                size INTEGER NOT NULL,
                encryption_method TEXT NOT NULL,
                folder_id INTEGER,
                expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (folder_id) REFERENCES folders (id)
            )
        ''')
        
        # Share links table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS share_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id TEXT NOT NULL,
                share_token TEXT UNIQUE NOT NULL,
                share_password TEXT,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                access_count INTEGER DEFAULT 0,
                is_revoked INTEGER DEFAULT 0,
                FOREIGN KEY (file_id) REFERENCES files (file_id)
            )
        ''')
        
        # Share access log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS share_access_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                share_token TEXT NOT NULL,
                accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                FOREIGN KEY (share_token) REFERENCES share_links (share_token)
            )
        ''')
        
        # Teams table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                owner_id INTEGER NOT NULL,
                max_members INTEGER DEFAULT 8,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner_id) REFERENCES users (id)
            )
        ''')
        
        # Team members table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS team_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'editor', 'viewer')),
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (team_id) REFERENCES teams (id),
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(team_id, user_id)
            )
        ''')
        
        # Team settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS team_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER UNIQUE NOT NULL,
                require_2fa INTEGER DEFAULT 0,
                max_file_size INTEGER DEFAULT 104857600,
                FOREIGN KEY (team_id) REFERENCES teams (id)
            )
        ''')
        
        # Folders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS folders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                parent_id INTEGER,
                encryption_password TEXT,
                created_by INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (team_id) REFERENCES teams (id),
                FOREIGN KEY (parent_id) REFERENCES folders (id),
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # Folder permissions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS folder_permissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                folder_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                can_read INTEGER DEFAULT 1,
                can_write INTEGER DEFAULT 0,
                can_delete INTEGER DEFAULT 0,
                FOREIGN KEY (folder_id) REFERENCES folders (id),
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(folder_id, user_id)
            )
        ''')
        
        # Invitations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invitations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER NOT NULL,
                email TEXT,
                token TEXT UNIQUE NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                used INTEGER DEFAULT 0,
                created_by INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (team_id) REFERENCES teams (id),
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # Audit log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                entity_type TEXT,
                entity_id TEXT,
                details TEXT,
                ip_address TEXT,
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # File requests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token TEXT UNIQUE NOT NULL,
                requested_by INTEGER NOT NULL,
                team_id INTEGER,
                max_files INTEGER DEFAULT 1,
                files_uploaded INTEGER DEFAULT 0,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (requested_by) REFERENCES users (id),
                FOREIGN KEY (team_id) REFERENCES teams (id)
            )
        ''')
        
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Tags table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # File tags junction table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_tags (
                file_id TEXT NOT NULL,
                tag_id INTEGER NOT NULL,
                FOREIGN KEY (file_id) REFERENCES files (file_id),
                FOREIGN KEY (tag_id) REFERENCES tags (id),
                PRIMARY KEY (file_id, tag_id)
            )
        ''')
        
        # Notifications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                link TEXT,
                is_read INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # ─────────────────────────────────────────────────────────────
    # USER OPERATIONS
    # ─────────────────────────────────────────────────────────────
    def create_user(self, username, password, first_name, last_name):
        """Create new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        hashed_password = generate_password_hash(password)
        
        cursor.execute('''
            INSERT INTO users (username, password, first_name, last_name)
            VALUES (?, ?, ?, ?)
        ''', (username, hashed_password, first_name, last_name))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return user_id
    
    def get_user_by_username(self, username):
        """Get user by username"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        conn.close()
        
        return dict(user) if user else None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        
        conn.close()
        
        return dict(user) if user else None
    
    # ─────────────────────────────────────────────────────────────
    # FILE OPERATIONS
    # ─────────────────────────────────────────────────────────────
    def add_file(self, user_id, file_id, original_name, encrypted_name, size, encryption_method):
        """Add encrypted file to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO files (user_id, file_id, original_name, encrypted_name, size, encryption_method)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, file_id, original_name, encrypted_name, size, encryption_method))
        
        conn.commit()
        conn.close()
    
    def get_user_files(self, user_id):
        """Get all files for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM files 
            WHERE user_id = ? 
            ORDER BY created_at DESC
        ''', (user_id,))
        
        files = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return files
    
    def get_file(self, file_id, user_id):
        """Get specific file for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM files 
            WHERE file_id = ? AND user_id = ?
        ''', (file_id, user_id))
        
        file = cursor.fetchone()
        
        conn.close()
        
        return dict(file) if file else None
    
    def get_file_by_id(self, file_id):
        """Get file by file_id (without user check)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM files WHERE file_id = ?', (file_id,))
        file = cursor.fetchone()
        
        conn.close()
        
        return dict(file) if file else None
    
    def delete_file(self, file_id, user_id):
        """Delete file"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM files 
            WHERE file_id = ? AND user_id = ?
        ''', (file_id, user_id))
        
        conn.commit()
        conn.close()
    
    # ─────────────────────────────────────────────────────────────
    # SHARE OPERATIONS
    # ─────────────────────────────────────────────────────────────
    def create_share_link(self, file_id, share_token, expires_at, share_password=''):
        """Create share link for file"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO share_links (file_id, share_token, share_password, expires_at)
            VALUES (?, ?, ?, ?)
        ''', (file_id, share_token, share_password, expires_at))
        
        conn.commit()
        conn.close()
    
    def get_share_link(self, share_token):
        """Get share link info"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT sl.*, f.original_name, f.size, f.encryption_method
            FROM share_links sl
            JOIN files f ON sl.file_id = f.file_id
            WHERE sl.share_token = ?
        ''', (share_token,))
        
        share = cursor.fetchone()
        
        conn.close()
        
        if share:
            result = dict(share)
            # Convert string to datetime
            result['expires_at'] = datetime.fromisoformat(result['expires_at'])
            return result
        
        return None
    
    def track_share_access(self, share_token, ip_address=''):
        """Track when share link is accessed"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Log access
        cursor.execute('''
            INSERT INTO share_access_log (share_token, ip_address)
            VALUES (?, ?)
        ''', (share_token, ip_address))
        
        # Increment counter
        cursor.execute('''
            UPDATE share_links 
            SET access_count = access_count + 1
            WHERE share_token = ?
        ''', (share_token,))
        
        conn.commit()
        conn.close()
    
    def get_file_shares(self, file_id):
        """Get all share links for a file"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM share_links 
            WHERE file_id = ?
            ORDER BY created_at DESC
        ''', (file_id,))
        
        shares = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return shares
    
    # ─────────────────────────────────────────────────────────────
    # STATISTICS
    # ─────────────────────────────────────────────────────────────
    def get_user_stats(self, user_id):
        """Get user statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total files
        cursor.execute('SELECT COUNT(*) as count FROM files WHERE user_id = ?', (user_id,))
        total_files = cursor.fetchone()['count']
        
        # Total size
        cursor.execute('SELECT SUM(size) as total FROM files WHERE user_id = ?', (user_id,))
        total_size = cursor.fetchone()['total'] or 0
        
        # Files by encryption method
        cursor.execute('''
            SELECT encryption_method, COUNT(*) as count 
            FROM files 
            WHERE user_id = ? 
            GROUP BY encryption_method
        ''', (user_id,))
        
        by_method = {row['encryption_method']: row['count'] for row in cursor.fetchall()}
        
        # Total shares
        cursor.execute('''
            SELECT COUNT(*) as count 
            FROM share_links sl
            JOIN files f ON sl.file_id = f.file_id
            WHERE f.user_id = ?
        ''', (user_id,))
        
        total_shares = cursor.fetchone()['count']
        
        conn.close()
        
        return {
            'total_files': total_files,
            'total_size': total_size,
            'by_method': by_method,
            'total_shares': total_shares
        }

    # ─────────────────────────────────────────────────────────────
    # TEAM OPERATIONS
    # ─────────────────────────────────────────────────────────────
    def create_team(self, name, owner_id):
        """Create a new team"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO teams (name, owner_id)
            VALUES (?, ?)
        ''', (name, owner_id))
        
        team_id = cursor.lastrowid
        
        # Add owner as admin member
        cursor.execute('''
            INSERT INTO team_members (team_id, user_id, role)
            VALUES (?, ?, 'admin')
        ''', (team_id, owner_id))
        
        # Create default team settings
        cursor.execute('''
            INSERT INTO team_settings (team_id)
            VALUES (?)
        ''', (team_id,))
        
        conn.commit()
        conn.close()
        
        return team_id
    
    def get_user_teams(self, user_id):
        """Get all teams user is member of"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.*, tm.role, u.username as owner_username
            FROM teams t
            JOIN team_members tm ON t.id = tm.team_id
            JOIN users u ON t.owner_id = u.id
            WHERE tm.user_id = ?
            ORDER BY t.created_at DESC
        ''', (user_id,))
        
        teams = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return teams
    
    def get_team(self, team_id):
        """Get team by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM teams WHERE id = ?', (team_id,))
        team = cursor.fetchone()
        
        conn.close()
        
        return dict(team) if team else None
    
    def get_team_members(self, team_id):
        """Get all members of a team"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.id, u.username, u.first_name, u.last_name, u.email,
                   tm.role, tm.joined_at, u.last_login
            FROM team_members tm
            JOIN users u ON tm.user_id = u.id
            WHERE tm.team_id = ?
            ORDER BY tm.joined_at ASC
        ''', (team_id,))
        
        members = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return members
    
    def is_team_member(self, team_id, user_id):
        """Check if user is member of team"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT role FROM team_members
            WHERE team_id = ? AND user_id = ?
        ''', (team_id, user_id))
        
        result = cursor.fetchone()
        conn.close()
        
        return dict(result) if result else None
    
    def update_member_role(self, team_id, user_id, new_role):
        """Update team member role"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE team_members
            SET role = ?
            WHERE team_id = ? AND user_id = ?
        ''', (new_role, team_id, user_id))
        
        conn.commit()
        conn.close()
    
    def remove_team_member(self, team_id, user_id):
        """Remove member from team"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM team_members
            WHERE team_id = ? AND user_id = ?
        ''', (team_id, user_id))
        
        conn.commit()
        conn.close()
    
    def get_team_settings(self, team_id):
        """Get team settings"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM team_settings WHERE team_id = ?', (team_id,))
        settings = cursor.fetchone()
        
        conn.close()
        
        return dict(settings) if settings else None
    
    def update_team_settings(self, team_id, **kwargs):
        """Update team settings"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        for key, value in kwargs.items():
            cursor.execute(f'''
                UPDATE team_settings
                SET {key} = ?
                WHERE team_id = ?
            ''', (value, team_id))
        
        conn.commit()
        conn.close()
    
    # ─────────────────────────────────────────────────────────────
    # FOLDER OPERATIONS
    # ─────────────────────────────────────────────────────────────
    def create_folder(self, team_id, name, created_by, parent_id=None, encryption_password=''):
        """Create a new folder"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO folders (team_id, name, parent_id, encryption_password, created_by)
            VALUES (?, ?, ?, ?, ?)
        ''', (team_id, name, parent_id, encryption_password, created_by))
        
        folder_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return folder_id
    
    def get_team_folders(self, team_id, parent_id=None):
        """Get folders in a team"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if parent_id is None:
            cursor.execute('''
                SELECT f.*, u.username as created_by_username
                FROM folders f
                JOIN users u ON f.created_by = u.id
                WHERE f.team_id = ? AND f.parent_id IS NULL
                ORDER BY f.created_at DESC
            ''', (team_id,))
        else:
            cursor.execute('''
                SELECT f.*, u.username as created_by_username
                FROM folders f
                JOIN users u ON f.created_by = u.id
                WHERE f.team_id = ? AND f.parent_id = ?
                ORDER BY f.created_at DESC
            ''', (team_id, parent_id))
        
        folders = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return folders
    
    def get_folder(self, folder_id):
        """Get folder by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM folders WHERE id = ?', (folder_id,))
        folder = cursor.fetchone()
        
        conn.close()
        
        return dict(folder) if folder else None
    
    def get_folder_files(self, folder_id):
        """Get all files in a folder"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM files
            WHERE folder_id = ?
            ORDER BY created_at DESC
        ''', (folder_id,))
        
        files = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return files
    
    def set_folder_permission(self, folder_id, user_id, can_read=1, can_write=0, can_delete=0):
        """Set folder permissions for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO folder_permissions
            (folder_id, user_id, can_read, can_write, can_delete)
            VALUES (?, ?, ?, ?, ?)
        ''', (folder_id, user_id, can_read, can_write, can_delete))
        
        conn.commit()
        conn.close()
    
    def get_folder_permissions(self, folder_id, user_id):
        """Get user's permissions for a folder"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM folder_permissions
            WHERE folder_id = ? AND user_id = ?
        ''', (folder_id, user_id))
        
        perms = cursor.fetchone()
        conn.close()
        
        return dict(perms) if perms else None
    
    # ─────────────────────────────────────────────────────────────
    # INVITATION OPERATIONS
    # ─────────────────────────────────────────────────────────────
    def create_invitation(self, team_id, created_by, email='', expires_hours=48):
        """Create team invitation"""
        import secrets
        from datetime import timedelta
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=expires_hours)
        
        cursor.execute('''
            INSERT INTO invitations (team_id, email, token, expires_at, created_by)
            VALUES (?, ?, ?, ?, ?)
        ''', (team_id, email, token, expires_at, created_by))
        
        conn.commit()
        conn.close()
        
        return token
    
    def get_invitation(self, token):
        """Get invitation by token"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT i.*, t.name as team_name
            FROM invitations i
            JOIN teams t ON i.team_id = t.id
            WHERE i.token = ? AND i.used = 0
        ''', (token,))
        
        invitation = cursor.fetchone()
        conn.close()
        
        if invitation:
            result = dict(invitation)
            result['expires_at'] = datetime.fromisoformat(result['expires_at'])
            return result
        
        return None
    
    def use_invitation(self, token, user_id):
        """Mark invitation as used and add user to team"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get invitation
        cursor.execute('SELECT team_id FROM invitations WHERE token = ?', (token,))
        inv = cursor.fetchone()
        
        if not inv:
            conn.close()
            return False
        
        team_id = inv['team_id']
        
        # Add user to team
        cursor.execute('''
            INSERT OR IGNORE INTO team_members (team_id, user_id, role)
            VALUES (?, ?, 'viewer')
        ''', (team_id, user_id))
        
        # Mark invitation as used
        cursor.execute('''
            UPDATE invitations
            SET used = 1
            WHERE token = ?
        ''', (token,))
        
        conn.commit()
        conn.close()
        
        return True
    
    # ─────────────────────────────────────────────────────────────
    # AUDIT LOG OPERATIONS
    # ─────────────────────────────────────────────────────────────
    def log_action(self, user_id, action, entity_type='', entity_id='', details='', ip_address='', user_agent=''):
        """Log an action to audit log"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO audit_log (user_id, action, entity_type, entity_id, details, ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, action, entity_type, entity_id, details, ip_address, user_agent))
        
        conn.commit()
        conn.close()
    
    def get_audit_logs(self, team_id=None, user_id=None, limit=100, offset=0):
        """Get audit logs with optional filters"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT al.*, u.username, u.first_name, u.last_name
            FROM audit_log al
            LEFT JOIN users u ON al.user_id = u.id
            WHERE 1=1
        '''
        params = []
        
        if user_id:
            query += ' AND al.user_id = ?'
            params.append(user_id)
        
        query += ' ORDER BY al.created_at DESC LIMIT ? OFFSET ?'
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        logs = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return logs
    
    def get_team_activity(self, team_id, limit=50):
        """Get recent activity for a team"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT al.*, u.username, u.first_name, u.last_name
            FROM audit_log al
            JOIN users u ON al.user_id = u.id
            JOIN team_members tm ON u.id = tm.user_id
            WHERE tm.team_id = ?
            ORDER BY al.created_at DESC
            LIMIT ?
        ''', (team_id, limit))
        
        activity = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return activity
    
    # ─────────────────────────────────────────────────────────────
    # FILE REQUEST OPERATIONS
    # ─────────────────────────────────────────────────────────────
    def create_file_request(self, requested_by, team_id=None, max_files=1, expires_hours=48):
        """Create a file upload request"""
        import secrets
        from datetime import timedelta
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=expires_hours)
        
        cursor.execute('''
            INSERT INTO file_requests (token, requested_by, team_id, max_files, expires_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (token, requested_by, team_id, max_files, expires_at))
        
        conn.commit()
        conn.close()
        
        return token
    
    def get_file_request(self, token):
        """Get file request by token"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM file_requests WHERE token = ?', (token,))
        request = cursor.fetchone()
        
        conn.close()
        
        if request:
            result = dict(request)
            result['expires_at'] = datetime.fromisoformat(result['expires_at'])
            return result
        
        return None
    
    def increment_file_request_count(self, token):
        """Increment uploaded files count for a request"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE file_requests
            SET files_uploaded = files_uploaded + 1
            WHERE token = ?
        ''', (token,))
        
        conn.commit()
        conn.close()
    
    # ─────────────────────────────────────────────────────────────
    # SESSION OPERATIONS
    # ─────────────────────────────────────────────────────────────
    def create_session(self, user_id, session_token, ip_address='', user_agent=''):
        """Create a new session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sessions (user_id, session_token, ip_address, user_agent)
            VALUES (?, ?, ?, ?)
        ''', (user_id, session_token, ip_address, user_agent))
        
        conn.commit()
        conn.close()
    
    def get_user_sessions(self, user_id):
        """Get all active sessions for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM sessions
            WHERE user_id = ?
            ORDER BY last_active DESC
        ''', (user_id,))
        
        sessions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return sessions
    
    def update_session_activity(self, session_token):
        """Update session last active time"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE sessions
            SET last_active = CURRENT_TIMESTAMP
            WHERE session_token = ?
        ''', (session_token,))
        
        conn.commit()
        conn.close()
    
    def revoke_session(self, session_token):
        """Revoke a session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM sessions WHERE session_token = ?', (session_token,))
        
        conn.commit()
        conn.close()
    
    # ─────────────────────────────────────────────────────────────
    # TAG OPERATIONS
    # ─────────────────────────────────────────────────────────────
    def create_tag(self, name):
        """Create a new tag"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('INSERT OR IGNORE INTO tags (name) VALUES (?)', (name.lower(),))
        
        cursor.execute('SELECT id FROM tags WHERE name = ?', (name.lower(),))
        tag_id = cursor.fetchone()['id']
        
        conn.commit()
        conn.close()
        
        return tag_id
    
    def add_file_tag(self, file_id, tag_name):
        """Add tag to file"""
        tag_id = self.create_tag(tag_name)
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR IGNORE INTO file_tags (file_id, tag_id)
            VALUES (?, ?)
        ''', (file_id, tag_id))
        
        conn.commit()
        conn.close()
    
    def get_file_tags(self, file_id):
        """Get all tags for a file"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.* FROM tags t
            JOIN file_tags ft ON t.id = ft.tag_id
            WHERE ft.file_id = ?
        ''', (file_id,))
        
        tags = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return tags
    
    def search_files(self, user_id, query='', tag='', method='', date_from='', date_to=''):
        """Advanced file search"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        sql = 'SELECT DISTINCT f.* FROM files f LEFT JOIN file_tags ft ON f.file_id = ft.file_id LEFT JOIN tags t ON ft.tag_id = t.id WHERE f.user_id = ?'
        params = [user_id]
        
        if query:
            sql += ' AND f.original_name LIKE ?'
            params.append(f'%{query}%')
        
        if tag:
            sql += ' AND t.name = ?'
            params.append(tag.lower())
        
        if method:
            sql += ' AND f.encryption_method = ?'
            params.append(method)
        
        if date_from:
            sql += ' AND f.created_at >= ?'
            params.append(date_from)
        
        if date_to:
            sql += ' AND f.created_at <= ?'
            params.append(date_to)
        
        sql += ' ORDER BY f.created_at DESC'
        
        cursor.execute(sql, params)
        files = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return files
    
    # ─────────────────────────────────────────────────────────────
    # NOTIFICATION OPERATIONS
    # ─────────────────────────────────────────────────────────────
    def create_notification(self, user_id, type, title, message, link=''):
        """Create a notification"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO notifications (user_id, type, title, message, link)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, type, title, message, link))
        
        conn.commit()
        conn.close()
    
    def get_user_notifications(self, user_id, unread_only=False, limit=50):
        """Get user notifications"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        sql = 'SELECT * FROM notifications WHERE user_id = ?'
        params = [user_id]
        
        if unread_only:
            sql += ' AND is_read = 0'
        
        sql += ' ORDER BY created_at DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(sql, params)
        notifications = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return notifications
    
    def get_unread_count(self, user_id):
        """Get count of unread notifications"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as count FROM notifications WHERE user_id = ? AND is_read = 0', (user_id,))
        count = cursor.fetchone()['count']
        
        conn.close()
        
        return count
    
    def mark_notification_read(self, notification_id):
        """Mark notification as read"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE notifications SET is_read = 1 WHERE id = ?', (notification_id,))
        
        conn.commit()
        conn.close()
    
    def mark_all_notifications_read(self, user_id):
        """Mark all notifications as read for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE notifications SET is_read = 1 WHERE user_id = ?', (user_id,))
        
        conn.commit()
        conn.close()
    
    # ─────────────────────────────────────────────────────────────
    # ANALYTICS OPERATIONS
    # ─────────────────────────────────────────────────────────────
    def get_team_analytics(self, team_id):
        """Get analytics data for a team"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Files uploaded over time (last 30 days)
        cursor.execute('''
            SELECT DATE(f.created_at) as date, COUNT(*) as count
            FROM files f
            JOIN team_members tm ON f.user_id = tm.user_id
            WHERE tm.team_id = ? AND f.created_at >= date('now', '-30 days')
            GROUP BY DATE(f.created_at)
            ORDER BY date ASC
        ''', (team_id,))
        
        files_over_time = [dict(row) for row in cursor.fetchall()]
        
        # Encryption method breakdown
        cursor.execute('''
            SELECT f.encryption_method, COUNT(*) as count
            FROM files f
            JOIN team_members tm ON f.user_id = tm.user_id
            WHERE tm.team_id = ?
            GROUP BY f.encryption_method
        ''', (team_id,))
        
        encryption_breakdown = [dict(row) for row in cursor.fetchall()]
        
        # Storage per member
        cursor.execute('''
            SELECT u.username, u.first_name, u.last_name, 
                   COUNT(f.id) as file_count, SUM(f.size) as total_size
            FROM team_members tm
            JOIN users u ON tm.user_id = u.id
            LEFT JOIN files f ON u.id = f.user_id
            WHERE tm.team_id = ?
            GROUP BY u.id
        ''', (team_id,))
        
        storage_per_member = [dict(row) for row in cursor.fetchall()]
        
        # Share link usage
        cursor.execute('''
            SELECT COUNT(*) as total_shares, SUM(access_count) as total_accesses
            FROM share_links sl
            JOIN files f ON sl.file_id = f.file_id
            JOIN team_members tm ON f.user_id = tm.user_id
            WHERE tm.team_id = ?
        ''', (team_id,))
        
        share_stats = dict(cursor.fetchone())
        
        conn.close()
        
        return {
            'files_over_time': files_over_time,
            'encryption_breakdown': encryption_breakdown,
            'storage_per_member': storage_per_member,
            'share_stats': share_stats
        }
    
    # ─────────────────────────────────────────────────────────────
    # USER PROFILE OPERATIONS
    # ─────────────────────────────────────────────────────────────
    def update_user_profile(self, user_id, **kwargs):
        """Update user profile"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        allowed_fields = ['first_name', 'last_name', 'email', 'preferred_language']
        
        for key, value in kwargs.items():
            if key in allowed_fields:
                cursor.execute(f'''
                    UPDATE users
                    SET {key} = ?
                    WHERE id = ?
                ''', (value, user_id))
        
        conn.commit()
        conn.close()
    
    def update_user_password(self, user_id, new_password):
        """Update user password"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        hashed_password = generate_password_hash(new_password)
        
        cursor.execute('''
            UPDATE users
            SET password = ?
            WHERE id = ?
        ''', (hashed_password, user_id))
        
        conn.commit()
        conn.close()
    
    def enable_2fa(self, user_id, totp_secret):
        """Enable 2FA for user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users
            SET require_2fa = 1, totp_secret = ?
            WHERE id = ?
        ''', (totp_secret, user_id))
        
        conn.commit()
        conn.close()
    
    def disable_2fa(self, user_id):
        """Disable 2FA for user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users
            SET require_2fa = 0, totp_secret = NULL
            WHERE id = ?
        ''', (user_id,))
        
        conn.commit()
        conn.close()
    
    def deactivate_user(self, user_id):
        """Deactivate user account"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users
            SET is_active = 0
            WHERE id = ?
        ''', (user_id,))
        
        conn.commit()
        conn.close()
    
    def delete_user_account(self, user_id):
        """Delete user account and all associated data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Delete user's files
        cursor.execute('DELETE FROM files WHERE user_id = ?', (user_id,))
        
        # Remove from teams
        cursor.execute('DELETE FROM team_members WHERE user_id = ?', (user_id,))
        
        # Delete notifications
        cursor.execute('DELETE FROM notifications WHERE user_id = ?', (user_id,))
        
        # Delete sessions
        cursor.execute('DELETE FROM sessions WHERE user_id = ?', (user_id,))
        
        # Delete user
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        
        conn.commit()
        conn.close()
    
    def update_last_login(self, user_id):
        """Update user's last login timestamp"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users
            SET last_login = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (user_id,))
        
        conn.commit()
        conn.close()
    
    def revoke_all_share_links(self, user_id):
        """Revoke all share links for a user's files"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE share_links
            SET is_revoked = 1
            WHERE file_id IN (SELECT file_id FROM files WHERE user_id = ?)
        ''', (user_id,))
        
        conn.commit()
        conn.close()
