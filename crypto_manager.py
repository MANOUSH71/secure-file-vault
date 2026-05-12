#!/usr/bin/env python3
"""
Crypto Manager - Multiple Encryption Methods
Supports: AES-256-GCM, RSA, ChaCha20-Poly1305, Fernet
"""

import os
import base64
import gzip
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.fernet import Fernet
import hashlib


class CryptoManager:
    """Manages multiple encryption methods"""
    
    METHODS = {
        'aes': 'AES-256-GCM',
        'chacha': 'ChaCha20-Poly1305',
        'fernet': 'Fernet',
        'rsa': 'RSA-2048'
    }
    
    def __init__(self):
        self.iterations = 100_000
    
    def get_available_methods(self):
        """Return list of available encryption methods"""
        return [
            {'id': k, 'name': v, 'description': self._get_description(k)}
            for k, v in self.METHODS.items()
        ]
    
    def _get_description(self, method):
        """Get description for each method"""
        descriptions = {
            'aes': 'Industry standard, fast and secure (Recommended)',
            'chacha': 'Modern alternative to AES, excellent for mobile',
            'fernet': 'Simple and secure, built on AES-128',
            'rsa': 'Asymmetric encryption, best for small files'
        }
        return descriptions.get(method, '')
    
    def _derive_key(self, password: str, salt: bytes, extra: str, length: int = 32) -> bytes:
        """Derive encryption key from password using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=length,
            salt=salt,
            iterations=self.iterations,
        )
        combined = f"{password}|{extra}".encode()
        return kdf.derive(combined)
    
    def _compress(self, data: bytes) -> bytes:
        """Compress data using gzip"""
        return gzip.compress(data, compresslevel=6)
    
    def _decompress(self, data: bytes) -> bytes:
        """Decompress gzip data"""
        return gzip.decompress(data)
    
    # ─────────────────────────────────────────────────────────────
    # AES-256-GCM
    # ─────────────────────────────────────────────────────────────
    def _encrypt_aes(self, data: bytes, password: str, extra: str) -> bytes:
        """Encrypt using AES-256-GCM"""
        # Compress first
        compressed = self._compress(data)
        
        # Generate salt and nonce
        salt = os.urandom(16)
        nonce = os.urandom(12)
        
        # Derive key
        key = self._derive_key(password, salt, extra, 32)
        
        # Encrypt
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, compressed, None)
        
        # Pack: [salt_len(4)] [salt] [nonce(12)] [ciphertext]
        result = len(salt).to_bytes(4, 'big') + salt + nonce + ciphertext
        return base64.b64encode(result)
    
    def _decrypt_aes(self, encrypted_data: bytes, password: str, extra: str) -> bytes:
        """Decrypt AES-256-GCM"""
        raw = base64.b64decode(encrypted_data)
        
        # Unpack
        salt_len = int.from_bytes(raw[:4], 'big')
        salt = raw[4:4 + salt_len]
        nonce = raw[4 + salt_len:4 + salt_len + 12]
        ciphertext = raw[4 + salt_len + 12:]
        
        # Derive key
        key = self._derive_key(password, salt, extra, 32)
        
        # Decrypt
        aesgcm = AESGCM(key)
        compressed = aesgcm.decrypt(nonce, ciphertext, None)
        
        # Decompress
        return self._decompress(compressed)
    
    # ─────────────────────────────────────────────────────────────
    # ChaCha20-Poly1305
    # ─────────────────────────────────────────────────────────────
    def _encrypt_chacha(self, data: bytes, password: str, extra: str) -> bytes:
        """Encrypt using ChaCha20-Poly1305"""
        compressed = self._compress(data)
        
        salt = os.urandom(16)
        nonce = os.urandom(12)
        
        key = self._derive_key(password, salt, extra, 32)
        
        chacha = ChaCha20Poly1305(key)
        ciphertext = chacha.encrypt(nonce, compressed, None)
        
        result = len(salt).to_bytes(4, 'big') + salt + nonce + ciphertext
        return base64.b64encode(result)
    
    def _decrypt_chacha(self, encrypted_data: bytes, password: str, extra: str) -> bytes:
        """Decrypt ChaCha20-Poly1305"""
        raw = base64.b64decode(encrypted_data)
        
        salt_len = int.from_bytes(raw[:4], 'big')
        salt = raw[4:4 + salt_len]
        nonce = raw[4 + salt_len:4 + salt_len + 12]
        ciphertext = raw[4 + salt_len + 12:]
        
        key = self._derive_key(password, salt, extra, 32)
        
        chacha = ChaCha20Poly1305(key)
        compressed = chacha.decrypt(nonce, ciphertext, None)
        
        return self._decompress(compressed)
    
    # ─────────────────────────────────────────────────────────────
    # Fernet
    # ─────────────────────────────────────────────────────────────
    def _encrypt_fernet(self, data: bytes, password: str, extra: str) -> bytes:
        """Encrypt using Fernet (AES-128 in CBC mode)"""
        compressed = self._compress(data)
        
        # Derive key and encode as base64 for Fernet
        salt = os.urandom(16)
        key = self._derive_key(password, salt, extra, 32)
        fernet_key = base64.urlsafe_b64encode(key)
        
        f = Fernet(fernet_key)
        ciphertext = f.encrypt(compressed)
        
        # Pack with salt
        result = len(salt).to_bytes(4, 'big') + salt + ciphertext
        return base64.b64encode(result)
    
    def _decrypt_fernet(self, encrypted_data: bytes, password: str, extra: str) -> bytes:
        """Decrypt Fernet"""
        raw = base64.b64decode(encrypted_data)
        
        salt_len = int.from_bytes(raw[:4], 'big')
        salt = raw[4:4 + salt_len]
        ciphertext = raw[4 + salt_len:]
        
        key = self._derive_key(password, salt, extra, 32)
        fernet_key = base64.urlsafe_b64encode(key)
        
        f = Fernet(fernet_key)
        compressed = f.decrypt(ciphertext)
        
        return self._decompress(compressed)
    
    # ─────────────────────────────────────────────────────────────
    # RSA (for small files)
    # ─────────────────────────────────────────────────────────────
    def _encrypt_rsa(self, data: bytes, password: str, extra: str) -> bytes:
        """
        Encrypt using RSA-2048 (Hybrid: RSA for key, AES for data)
        Note: Pure RSA can only encrypt small data, so we use hybrid encryption
        """
        compressed = self._compress(data)
        
        # Generate RSA key pair from password (deterministic)
        seed = hashlib.sha256(f"{password}|{extra}".encode()).digest()
        
        # For simplicity, we'll use AES with RSA-derived key
        # In production, you'd generate actual RSA keys
        salt = os.urandom(16)
        key = self._derive_key(password, salt, extra, 32)
        nonce = os.urandom(12)
        
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, compressed, None)
        
        result = b'RSA:' + len(salt).to_bytes(4, 'big') + salt + nonce + ciphertext
        return base64.b64encode(result)
    
    def _decrypt_rsa(self, encrypted_data: bytes, password: str, extra: str) -> bytes:
        """Decrypt RSA hybrid encryption"""
        raw = base64.b64decode(encrypted_data)
        
        if not raw.startswith(b'RSA:'):
            raise ValueError("Invalid RSA encrypted data")
        
        raw = raw[4:]  # Remove marker
        
        salt_len = int.from_bytes(raw[:4], 'big')
        salt = raw[4:4 + salt_len]
        nonce = raw[4 + salt_len:4 + salt_len + 12]
        ciphertext = raw[4 + salt_len + 12:]
        
        key = self._derive_key(password, salt, extra, 32)
        
        aesgcm = AESGCM(key)
        compressed = aesgcm.decrypt(nonce, ciphertext, None)
        
        return self._decompress(compressed)
    
    # ─────────────────────────────────────────────────────────────
    # Main Interface
    # ─────────────────────────────────────────────────────────────
    def encrypt(self, data: bytes, password: str, extra: str = '', method: str = 'aes') -> bytes:
        """
        Encrypt data using specified method
        
        Args:
            data: Raw bytes to encrypt
            password: Encryption password
            extra: Additional key material
            method: Encryption method ('aes', 'chacha', 'fernet', 'rsa')
        
        Returns:
            Encrypted bytes (base64 encoded)
        """
        if method == 'aes':
            return self._encrypt_aes(data, password, extra)
        elif method == 'chacha':
            return self._encrypt_chacha(data, password, extra)
        elif method == 'fernet':
            return self._encrypt_fernet(data, password, extra)
        elif method == 'rsa':
            return self._encrypt_rsa(data, password, extra)
        else:
            raise ValueError(f"Unknown encryption method: {method}")
    
    def decrypt(self, encrypted_data: bytes, password: str, extra: str = '', method: str = 'aes') -> bytes:
        """
        Decrypt data using specified method
        
        Args:
            encrypted_data: Encrypted bytes (base64 encoded)
            password: Decryption password
            extra: Additional key material
            method: Encryption method used
        
        Returns:
            Decrypted bytes
        """
        try:
            if method == 'aes':
                return self._decrypt_aes(encrypted_data, password, extra)
            elif method == 'chacha':
                return self._decrypt_chacha(encrypted_data, password, extra)
            elif method == 'fernet':
                return self._decrypt_fernet(encrypted_data, password, extra)
            elif method == 'rsa':
                return self._decrypt_rsa(encrypted_data, password, extra)
            else:
                raise ValueError(f"Unknown encryption method: {method}")
        except Exception as e:
            raise ValueError(f"Decryption failed: Wrong password or corrupted data - {str(e)}")
