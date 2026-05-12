/**
 * Secure File Vault Pro - Crypto Module
 * Client-side encryption using Web Crypto API
 */

class CryptoManager {
    constructor() {
        this.iterations = 100000;
    }

    /**
     * Derive encryption key from password using PBKDF2
     */
    async deriveKey(password, salt, extraKey = '') {
        const combined = password + '|' + extraKey;
        const encoder = new TextEncoder();
        const keyMaterial = await crypto.subtle.importKey(
            'raw',
            encoder.encode(combined),
            'PBKDF2',
            false,
            ['deriveBits', 'deriveKey']
        );

        return await crypto.subtle.deriveKey(
            {
                name: 'PBKDF2',
                salt: salt,
                iterations: this.iterations,
                hash: 'SHA-256'
            },
            keyMaterial,
            { name: 'AES-GCM', length: 256 },
            false,
            ['encrypt', 'decrypt']
        );
    }

    /**
     * Compress data using pako (gzip)
     */
    compress(data) {
        // For simplicity, we'll skip compression in browser
        // You can add pako.js library for gzip compression
        return data;
    }

    /**
     * Decompress data
     */
    decompress(data) {
        return data;
    }

    /**
     * Encrypt file using AES-256-GCM
     */
    async encryptAES(fileData, password, extraKey = '') {
        try {
            // Generate salt and IV
            const salt = crypto.getRandomValues(new Uint8Array(16));
            const iv = crypto.getRandomValues(new Uint8Array(12));

            // Derive key
            const key = await this.deriveKey(password, salt, extraKey);

            // Encrypt
            const encrypted = await crypto.subtle.encrypt(
                {
                    name: 'AES-GCM',
                    iv: iv
                },
                key,
                fileData
            );

            // Pack: [salt(16)] [iv(12)] [encrypted data]
            const result = new Uint8Array(salt.length + iv.length + encrypted.byteLength);
            result.set(salt, 0);
            result.set(iv, salt.length);
            result.set(new Uint8Array(encrypted), salt.length + iv.length);

            return result;
        } catch (error) {
            throw new Error('Encryption failed: ' + error.message);
        }
    }

    /**
     * Decrypt file using AES-256-GCM
     */
    async decryptAES(encryptedData, password, extraKey = '') {
        try {
            // Unpack
            const salt = encryptedData.slice(0, 16);
            const iv = encryptedData.slice(16, 28);
            const ciphertext = encryptedData.slice(28);

            // Derive key
            const key = await this.deriveKey(password, salt, extraKey);

            // Decrypt
            const decrypted = await crypto.subtle.decrypt(
                {
                    name: 'AES-GCM',
                    iv: iv
                },
                key,
                ciphertext
            );

            return new Uint8Array(decrypted);
        } catch (error) {
            throw new Error('Decryption failed: Wrong password or corrupted data');
        }
    }

    /**
     * Encrypt file using ChaCha20-Poly1305 (simulated with AES-GCM)
     * Note: Web Crypto API doesn't support ChaCha20, so we use AES-GCM
     */
    async encryptChaCha(fileData, password, extraKey = '') {
        // Use AES-GCM as fallback (ChaCha20 not available in Web Crypto API)
        return await this.encryptAES(fileData, password, extraKey);
    }

    /**
     * Decrypt ChaCha20-Poly1305
     */
    async decryptChaCha(encryptedData, password, extraKey = '') {
        return await this.decryptAES(encryptedData, password, extraKey);
    }

    /**
     * Main encrypt function
     */
    async encrypt(fileData, password, extraKey = '', method = 'aes') {
        if (method === 'aes') {
            return await this.encryptAES(fileData, password, extraKey);
        } else if (method === 'chacha') {
            return await this.encryptChaCha(fileData, password, extraKey);
        } else {
            throw new Error('Unknown encryption method: ' + method);
        }
    }

    /**
     * Main decrypt function
     */
    async decrypt(encryptedData, password, extraKey = '', method = 'aes') {
        if (method === 'aes') {
            return await this.decryptAES(encryptedData, password, extraKey);
        } else if (method === 'chacha') {
            return await this.decryptChaCha(encryptedData, password, extraKey);
        } else {
            throw new Error('Unknown encryption method: ' + method);
        }
    }

    /**
     * Generate secure random token
     */
    generateToken(length = 32) {
        const array = new Uint8Array(length);
        crypto.getRandomValues(array);
        return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
    }

    /**
     * Hash password for storage
     */
    async hashPassword(password) {
        const encoder = new TextEncoder();
        const data = encoder.encode(password);
        const hash = await crypto.subtle.digest('SHA-256', data);
        return Array.from(new Uint8Array(hash))
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
    }
}

// Export for use in app.js
const cryptoManager = new CryptoManager();
