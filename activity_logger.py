#!/usr/bin/env python3
"""
Activity Logger - Track all user activities for security audit
"""

import sqlite3
from datetime import datetime
from pathlib import Path


class ActivityLogger:
    """Log all user activities"""
    
    def __init__(self, db_path='vault.db'):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize activity log table"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                activity_type TEXT NOT NULL,
                description TEXT,
                ip_address TEXT,
                user_agent TEXT,
                file_id TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create index for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_activity_user 
            ON activity_log(user_id, created_at DESC)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_activity_type 
            ON activity_log(activity_type, created_at DESC)
        ''')
        
        conn.commit()
        conn.close()
    
    def log(self, user_id, activity_type, description='', ip_address='', user_agent='', file_id='', status='success'):
        """
        Log an activity
        
        Activity types:
        - login, logout, register
        - file_upload, file_encrypt, file_decrypt, file_delete
        - share_create, share_access, share_download
        - password_change, settings_update
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO activity_log 
            (user_id, activity_type, description, ip_address, user_agent, file_id, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, activity_type, description, ip_address, user_agent, file_id, status))
        
        conn.commit()
        conn.close()
    
    def get_user_activities(self, user_id, limit=50):
        """Get recent activities for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM activity_log
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        activities = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return activities
    
    def get_file_activities(self, file_id, limit=20):
        """Get activities for a specific file"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT al.*, u.username, u.first_name, u.last_name
            FROM activity_log al
            LEFT JOIN users u ON al.user_id = u.id
            WHERE al.file_id = ?
            ORDER BY al.created_at DESC
            LIMIT ?
        ''', (file_id, limit))
        
        activities = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return activities
    
    def get_security_events(self, limit=100):
        """Get security-related events"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT al.*, u.username
            FROM activity_log al
            LEFT JOIN users u ON al.user_id = u.id
            WHERE al.activity_type IN ('login', 'logout', 'password_change', 'failed_login')
               OR al.status = 'failed'
            ORDER BY al.created_at DESC
            LIMIT ?
        ''', (limit,))
        
        events = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return events
    
    def get_activity_stats(self, user_id):
        """Get activity statistics for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total activities
        cursor.execute('SELECT COUNT(*) as total FROM activity_log WHERE user_id = ?', (user_id,))
        total = cursor.fetchone()['total']
        
        # Activities by type
        cursor.execute('''
            SELECT activity_type, COUNT(*) as count
            FROM activity_log
            WHERE user_id = ?
            GROUP BY activity_type
            ORDER BY count DESC
        ''', (user_id,))
        by_type = {row['activity_type']: row['count'] for row in cursor.fetchall()}
        
        # Recent activity (last 24 hours)
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM activity_log
            WHERE user_id = ?
            AND created_at >= datetime('now', '-1 day')
        ''', (user_id,))
        recent = cursor.fetchone()['count']
        
        # Failed activities
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM activity_log
            WHERE user_id = ?
            AND status = 'failed'
        ''', (user_id,))
        failed = cursor.fetchone()['count']
        
        conn.close()
        
        return {
            'total': total,
            'by_type': by_type,
            'recent_24h': recent,
            'failed': failed
        }
    
    def export_activities(self, user_id, output_file):
        """Export user activities to JSON file"""
        import json
        
        activities = self.get_user_activities(user_id, limit=1000)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(activities, f, indent=2, ensure_ascii=False, default=str)
        
        return len(activities)


# Test
if __name__ == "__main__":
    logger = ActivityLogger()
    print("📊 Activity Logger Ready!")
    print("\nActivity Types:")
    print("  • login, logout, register")
    print("  • file_upload, file_encrypt, file_decrypt, file_delete")
    print("  • share_create, share_access, share_download")
    print("  • password_change, settings_update")
