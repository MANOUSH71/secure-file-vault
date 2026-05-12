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
    async deriveKey(password, salt, extraKey = '', algorithm = 'AES-GCM') {
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
            { name: algorithm, length: 256 },
            false,
            ['encrypt', 'decrypt']
        );
    }

    /**
     * Encrypt file using AES-256-GCM
     */
    async encryptAES_GCM(fileData, password, extraKey = '') {
        try {
            const salt = crypto.getRandomValues(new Uint8Array(16));
            const iv = crypto.getRandomValues(new Uint8Array(12));
            const key = await this.deriveKey(password, salt, extraKey, 'AES-GCM');

            const encrypted = await crypto.subtle.encrypt(
                { name: 'AES-GCM', iv: iv },
                key,
                fileData
            );

            const result = new Uint8Array(salt.length + iv.length + encrypted.byteLength);
            result.set(salt, 0);
            result.set(iv, salt.length);
            result.set(new Uint8Array(encrypted), salt.length + iv.length);
            return result;
        } catch (error) {
            throw new Error('AES-GCM Encryption failed: ' + error.message);
        }
    }

    async decryptAES_GCM(encryptedData, password, extraKey = '') {
        try {
            const salt = encryptedData.slice(0, 16);
            const iv = encryptedData.slice(16, 28);
            const ciphertext = encryptedData.slice(28);
            const key = await this.deriveKey(password, salt, extraKey, 'AES-GCM');

            const decrypted = await crypto.subtle.decrypt(
                { name: 'AES-GCM', iv: iv },
                key,
                ciphertext
            );
            return new Uint8Array(decrypted);
        } catch (error) {
            throw new Error('AES-GCM Decryption failed: Wrong password or corrupted data');
        }
    }

    /**
     * Encrypt file using AES-256-CBC
     */
    async encryptAES_CBC(fileData, password, extraKey = '') {
        try {
            const salt = crypto.getRandomValues(new Uint8Array(16));
            const iv = crypto.getRandomValues(new Uint8Array(16)); // CBC uses 16 byte IV
            const key = await this.deriveKey(password, salt, extraKey, 'AES-CBC');

            const encrypted = await crypto.subtle.encrypt(
                { name: 'AES-CBC', iv: iv },
                key,
                fileData
            );

            const result = new Uint8Array(salt.length + iv.length + encrypted.byteLength);
            result.set(salt, 0);
            result.set(iv, salt.length);
            result.set(new Uint8Array(encrypted), salt.length + iv.length);
            return result;
        } catch (error) {
            throw new Error('AES-CBC Encryption failed: ' + error.message);
        }
    }

    async decryptAES_CBC(encryptedData, password, extraKey = '') {
        try {
            const salt = encryptedData.slice(0, 16);
            const iv = encryptedData.slice(16, 32);
            const ciphertext = encryptedData.slice(32);
            const key = await this.deriveKey(password, salt, extraKey, 'AES-CBC');

            const decrypted = await crypto.subtle.decrypt(
                { name: 'AES-CBC', iv: iv },
                key,
                ciphertext
            );
            return new Uint8Array(decrypted);
        } catch (error) {
            throw new Error('AES-CBC Decryption failed: Wrong password or corrupted data');
        }
    }

    /**
     * Encrypt file using AES-256-CTR
     */
    async encryptAES_CTR(fileData, password, extraKey = '') {
        try {
            const salt = crypto.getRandomValues(new Uint8Array(16));
            const counter = crypto.getRandomValues(new Uint8Array(16)); // CTR uses 16 byte counter
            const key = await this.deriveKey(password, salt, extraKey, 'AES-CTR');

            const encrypted = await crypto.subtle.encrypt(
                { name: 'AES-CTR', counter: counter, length: 64 },
                key,
                fileData
            );

            const result = new Uint8Array(salt.length + counter.length + encrypted.byteLength);
            result.set(salt, 0);
            result.set(counter, salt.length);
            result.set(new Uint8Array(encrypted), salt.length + counter.length);
            return result;
        } catch (error) {
            throw new Error('AES-CTR Encryption failed: ' + error.message);
        }
    }

    async decryptAES_CTR(encryptedData, password, extraKey = '') {
        try {
            const salt = encryptedData.slice(0, 16);
            const counter = encryptedData.slice(16, 32);
            const ciphertext = encryptedData.slice(32);
            const key = await this.deriveKey(password, salt, extraKey, 'AES-CTR');

            const decrypted = await crypto.subtle.decrypt(
                { name: 'AES-CTR', counter: counter, length: 64 },
                key,
                ciphertext
            );
            return new Uint8Array(decrypted);
        } catch (error) {
            throw new Error('AES-CTR Decryption failed: Wrong password or corrupted data');
        }
    }

    /**
     * Main encrypt function
     */
    async encrypt(fileData, password, extraKey = '', method = 'aes') {
        switch (method) {
            case 'aes':
            case 'aes-gcm':
                return await this.encryptAES_GCM(fileData, password, extraKey);
            case 'aes-cbc':
                return await this.encryptAES_CBC(fileData, password, extraKey);
            case 'aes-ctr':
                return await this.encryptAES_CTR(fileData, password, extraKey);
            case 'chacha':
                // Fallback as Web Crypto doesn't support ChaCha
                return await this.encryptAES_GCM(fileData, password, extraKey);
            default:
                throw new Error('Unknown encryption method: ' + method);
        }
    }

    /**
     * Main decrypt function
     */
    async decrypt(encryptedData, password, extraKey = '', method = 'aes') {
        switch (method) {
            case 'aes':
            case 'aes-gcm':
                return await this.decryptAES_GCM(encryptedData, password, extraKey);
            case 'aes-cbc':
                return await this.decryptAES_CBC(encryptedData, password, extraKey);
            case 'aes-ctr':
                return await this.decryptAES_CTR(encryptedData, password, extraKey);
            case 'chacha':
                return await this.decryptAES_GCM(encryptedData, password, extraKey);
            default:
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

const cryptoManager = new CryptoManager();
