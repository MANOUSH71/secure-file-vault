#!/usr/bin/env python3
"""
Two-Factor Authentication (2FA) Module
Using TOTP (Time-based One-Time Password)
"""

import pyotp
import qrcode
import io
import base64
from datetime import datetime


class TwoFactorAuth:
    """Handle 2FA operations"""
    
    def __init__(self, issuer_name="Secure File Vault Pro"):
        self.issuer_name = issuer_name
    
    def generate_secret(self):
        """Generate a new secret key for 2FA"""
        return pyotp.random_base32()
    
    def get_totp_uri(self, secret, username):
        """
        Get TOTP URI for QR code generation
        
        Args:
            secret: The secret key
            username: User's username or email
        
        Returns:
            TOTP URI string
        """
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(
            name=username,
            issuer_name=self.issuer_name
        )
    
    def generate_qr_code(self, secret, username):
        """
        Generate QR code as base64 image
        
        Returns:
            Base64 encoded QR code image
        """
        uri = self.get_totp_uri(secret, username)
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(uri)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_base64}"
    
    def verify_token(self, secret, token):
        """
        Verify a TOTP token
        
        Args:
            secret: The secret key
            token: 6-digit token from authenticator app
        
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            totp = pyotp.TOTP(secret)
            # Allow 1 time step before and after (30 seconds window)
            return totp.verify(token, valid_window=1)
        except:
            return False
    
    def get_current_token(self, secret):
        """
        Get current token (for testing)
        
        Args:
            secret: The secret key
        
        Returns:
            Current 6-digit token
        """
        totp = pyotp.TOTP(secret)
        return totp.now()
    
    def generate_backup_codes(self, count=10):
        """
        Generate backup codes for account recovery
        
        Returns:
            List of backup codes
        """
        import secrets
        import string
        
        codes = []
        for _ in range(count):
            # Generate 8-character alphanumeric code
            code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            # Format as XXXX-XXXX
            formatted = f"{code[:4]}-{code[4:]}"
            codes.append(formatted)
        
        return codes


# Database extension for 2FA
class TwoFactorAuthDB:
    """Database operations for 2FA"""
    
    def __init__(self, db_path='vault.db'):
        import sqlite3
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize 2FA tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 2FA settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_2fa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                secret TEXT NOT NULL,
                enabled BOOLEAN DEFAULT 0,
                backup_codes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def enable_2fa(self, user_id, secret, backup_codes):
        """Enable 2FA for a user"""
        import json
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        backup_codes_json = json.dumps(backup_codes)
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_2fa (user_id, secret, enabled, backup_codes)
            VALUES (?, ?, 1, ?)
        ''', (user_id, secret, backup_codes_json))
        
        conn.commit()
        conn.close()
    
    def disable_2fa(self, user_id):
        """Disable 2FA for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE user_2fa SET enabled = 0 WHERE user_id = ?', (user_id,))
        
        conn.commit()
        conn.close()
    
    def get_2fa_settings(self, user_id):
        """Get 2FA settings for a user"""
        import json
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM user_2fa WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            settings = dict(result)
            if settings['backup_codes']:
                settings['backup_codes'] = json.loads(settings['backup_codes'])
            return settings
        
        return None
    
    def use_backup_code(self, user_id, code):
        """Use a backup code (remove it after use)"""
        import json
        
        settings = self.get_2fa_settings(user_id)
        if not settings or not settings['backup_codes']:
            return False
        
        backup_codes = settings['backup_codes']
        
        if code in backup_codes:
            backup_codes.remove(code)
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE user_2fa 
                SET backup_codes = ?
                WHERE user_id = ?
            ''', (json.dumps(backup_codes), user_id))
            
            conn.commit()
            conn.close()
            
            return True
        
        return False


# Test
if __name__ == "__main__":
    tfa = TwoFactorAuth()
    
    print("🔐 Two-Factor Authentication Module Ready!")
    print("\nTest:")
    
    # Generate secret
    secret = tfa.generate_secret()
    print(f"Secret: {secret}")
    
    # Generate current token
    token = tfa.get_current_token(secret)
    print(f"Current Token: {token}")
    
    # Verify token
    is_valid = tfa.verify_token(secret, token)
    print(f"Token Valid: {is_valid}")
    
    # Generate backup codes
    backup_codes = tfa.generate_backup_codes(5)
    print(f"\nBackup Codes:")
    for code in backup_codes:
        print(f"  • {code}")
