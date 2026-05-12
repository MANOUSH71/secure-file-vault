/**
 * Secure File Vault Pro - Cloud Module (Firebase)
 */

class CloudManager {
    constructor() {
        this.db = null;
        this.storage = null;
        this.enabled = false;
        this.init();
    }

    init() {
        const config = this.getConfig();
        if (config && config.apiKey) {
            try {
                if (!firebase.apps.length) {
                    firebase.initializeApp(config);
                }
                this.db = firebase.database();
                this.storage = firebase.storage();
                this.enabled = true;
                console.log("Cloud Storage Enabled");
            } catch (error) {
                console.error("Firebase Init Error:", error);
            }
        }
    }

    getConfig() {
        const config = localStorage.getItem('vault_cloud_config');
        return config ? JSON.parse(config) : null;
    }

    saveConfig(config) {
        localStorage.setItem('vault_cloud_config', JSON.stringify(config));
        location.reload(); // Reload to initialize with new config
    }

    // ============================================
    // Database Operations (Files & Shares)
    // ============================================

    async saveFileMetadata(fileRecord) {
        if (!this.enabled) return;
        await this.db.ref('files/' + fileRecord.id).set(fileRecord);
    }

    async getFileMetadata(fileId) {
        if (!this.enabled) return null;
        const snapshot = await this.db.ref('files/' + fileId).once('value');
        return snapshot.val();
    }

    async saveShareMetadata(shareRecord) {
        if (!this.enabled) return;
        await this.db.ref('shares/' + shareRecord.token).set(shareRecord);
    }

    async getShareMetadata(token) {
        if (!this.enabled) return null;
        const snapshot = await this.db.ref('shares/' + token).once('value');
        return snapshot.val();
    }

    // ============================================
    // Storage Operations (Encrypted Blobs)
    // ============================================

    async uploadEncryptedFile(fileId, encryptedArrayBuffer) {
        if (!this.enabled) return null;
        const storageRef = this.storage.ref('encrypted_files/' + fileId);
        await storageRef.put(encryptedArrayBuffer);
        return await storageRef.getDownloadURL();
    }

    async downloadEncryptedFile(fileId) {
        if (!this.enabled) return null;
        const storageRef = this.storage.ref('encrypted_files/' + fileId);
        const url = await storageRef.getDownloadURL();
        const response = await fetch(url);
        return await response.arrayBuffer();
    }
}

const cloudManager = new CloudManager();
