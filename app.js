/**
 * Secure File Vault Pro - Main Application
 * Client-side file encryption and management
 */

// ============================================
// State Management
// ============================================

let currentUser = null;
let currentFile = null;
let currentFileId = null;
let files = [];

// ============================================
// LocalStorage Keys
// ============================================

const STORAGE_KEYS = {
    USERS: 'vault_users',
    FILES: 'vault_files',
    CURRENT_USER: 'vault_current_user',
    SHARES: 'vault_shares'
};

// ============================================
// Initialization
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
});

function checkAuth() {
    const userId = localStorage.getItem(STORAGE_KEYS.CURRENT_USER);
    if (userId) {
        const users = getUsers();
        currentUser = users.find(u => u.id === userId);
        if (currentUser) {
            showDashboard();
            return;
        }
    }
    showAuthPage();
}

// ============================================
// Authentication
// ============================================

function showLogin() {
    document.getElementById('loginForm').classList.add('active');
    document.getElementById('registerForm').classList.remove('active');
}

function showRegister() {
    document.getElementById('registerForm').classList.add('active');
    document.getElementById('loginForm').classList.remove('active');
}

async function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('loginUsername').value.trim();
    const password = document.getElementById('loginPassword').value;
    
    const users = getUsers();
    const passwordHash = await cryptoManager.hashPassword(password);
    const user = users.find(u => u.username === username && u.passwordHash === passwordHash);
    
    if (user) {
        currentUser = user;
        localStorage.setItem(STORAGE_KEYS.CURRENT_USER, user.id);
        showAlert('Login successful!', 'success');
        
        // Add audit log
        addAuditLog('login', 'User logged in');
        
        // Add notification
        addNotification('login', 'Welcome Back!', `You logged in at ${new Date().toLocaleTimeString()}`);
        
        showDashboard();
    } else {
        showAlert('Invalid username or password', 'error');
    }
}

async function handleRegister(event) {
    event.preventDefault();
    
    const firstName = document.getElementById('regFirstName').value.trim();
    const lastName = document.getElementById('regLastName').value.trim();
    const username = document.getElementById('regUsername').value.trim();
    const password = document.getElementById('regPassword').value;
    
    const users = getUsers();
    
    if (users.find(u => u.username === username)) {
        showAlert('Username already exists', 'error');
        return;
    }
    
    const passwordHash = await cryptoManager.hashPassword(password);
    
    const newUser = {
        id: cryptoManager.generateToken(16),
        username,
        firstName,
        lastName,
        passwordHash,
        createdAt: new Date().toISOString()
    };
    
    users.push(newUser);
    saveUsers(users);
    
    currentUser = newUser;
    localStorage.setItem(STORAGE_KEYS.CURRENT_USER, newUser.id);
    
    showAlert('Account created successfully!', 'success');
    showDashboard();
}

function handleLogout() {
    // Add audit log before logout
    addAuditLog('logout', 'User logged out');
    
    localStorage.removeItem(STORAGE_KEYS.CURRENT_USER);
    currentUser = null;
    files = [];
    showAuthPage();
    showAlert('Logged out successfully', 'info');
}

// ============================================
// Page Navigation
// ============================================

function showAuthPage() {
    document.getElementById('authPage').classList.add('active');
    document.getElementById('dashboardPage').classList.remove('active');
}

function showDashboard() {
    document.getElementById('authPage').classList.remove('active');
    document.getElementById('dashboardPage').classList.add('active');
    
    document.getElementById('userDisplay').textContent = 
        `${currentUser.firstName} ${currentUser.lastName}`;
    
    loadFiles();
    updateStats();
}

// ============================================
// File Operations
// ============================================

function handleDragOver(event) {
    event.preventDefault();
    document.getElementById('uploadArea').classList.add('drag-over');
}

function handleDragLeave(event) {
    event.preventDefault();
    document.getElementById('uploadArea').classList.remove('drag-over');
}

function handleDrop(event) {
    event.preventDefault();
    document.getElementById('uploadArea').classList.remove('drag-over');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

function handleFileSelect(event) {
    const files = event.target.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

function processFile(file) {
    if (file.size > 100 * 1024 * 1024) {
        showAlert('File too large. Maximum size is 100MB', 'error');
        return;
    }
    
    currentFile = file;
    
    document.getElementById('selectedFileName').textContent = file.name;
    document.getElementById('selectedFileSize').textContent = formatFileSize(file.size);
    document.getElementById('encryptForm').style.display = 'block';
}

function cancelUpload() {
    currentFile = null;
    document.getElementById('encryptForm').style.display = 'none';
    document.getElementById('fileInput').value = '';
}

async function encryptFile() {
    if (!currentFile) {
        showAlert('No file selected', 'error');
        return;
    }
    
    const password = document.getElementById('encryptPassword').value;
    const extraKey = document.getElementById('extraKey').value;
    const method = document.getElementById('encryptionMethod').value;
    
    if (!password || password.length < 8) {
        showAlert('Password must be at least 8 characters', 'error');
        return;
    }
    
    showLoading('Encrypting file...');
    
    try {
        // Read file
        const fileData = await readFileAsArrayBuffer(currentFile);
        
        // Encrypt
        const encryptedData = await cryptoManager.encrypt(
            new Uint8Array(fileData),
            password,
            extraKey,
            method
        );
        
        // Save encrypted file
        const fileId = cryptoManager.generateToken(16);
        const fileRecord = {
            id: fileId,
            userId: currentUser.id,
            originalName: currentFile.name,
            size: currentFile.size,
            encryptedSize: encryptedData.length,
            method: method,
            createdAt: new Date().toISOString(),
            encryptedData: arrayBufferToBase64(encryptedData)
        };
        
        const allFiles = getFiles();
        allFiles.push(fileRecord);
        saveFiles(allFiles);
        
        hideLoading();
        showAlert('File encrypted successfully!', 'success');
        
        // Add audit log
        addAuditLog('encrypt', `Encrypted file: ${currentFile.name}`);
        
        // Add notification
        addNotification('file_encrypted', 'File Encrypted', `Successfully encrypted: ${currentFile.name}`);
        
        cancelUpload();
        loadFiles();
        updateStats();
        
    } catch (error) {
        hideLoading();
        showAlert('Encryption failed: ' + error.message, 'error');
    }
}

async function decryptFile() {
    const password = document.getElementById('decryptPassword').value;
    const extraKey = document.getElementById('decryptExtraKey').value;
    
    if (!password) {
        showAlert('Password required', 'error');
        return;
    }
    
    showLoading('Decrypting file...');
    
    try {
        const allFiles = getFiles();
        const fileRecord = allFiles.find(f => f.id === currentFileId);
        
        if (!fileRecord) {
            throw new Error('File not found');
        }
        
        // Decrypt
        const encryptedData = base64ToArrayBuffer(fileRecord.encryptedData);
        const decryptedData = await cryptoManager.decrypt(
            new Uint8Array(encryptedData),
            password,
            extraKey,
            fileRecord.method
        );
        
        // Download
        downloadFile(decryptedData, fileRecord.originalName);
        
        hideLoading();
        closeDecryptModal();
        showAlert('File decrypted successfully!', 'success');
        
        // Add audit log
        addAuditLog('decrypt', `Decrypted file: ${fileRecord.originalName}`);
        
        // Add notification
        addNotification('file_decrypted', 'File Decrypted', `Successfully decrypted: ${fileRecord.originalName}`);
        
    } catch (error) {
        hideLoading();
        showAlert('Decryption failed: ' + error.message, 'error');
    }
}

function deleteFile(fileId) {
    if (!confirm('Are you sure you want to delete this file?')) {
        return;
    }
    
    const allFiles = getFiles();
    const file = allFiles.find(f => f.id === fileId);
    const filtered = allFiles.filter(f => f.id !== fileId);
    saveFiles(filtered);
    
    loadFiles();
    updateStats();
    showAlert('File deleted successfully', 'success');
    
    // Add audit log
    if (file) {
        addAuditLog('delete', `Deleted file: ${file.originalName}`);
        
        // Add notification
        addNotification('file_deleted', 'File Deleted', `Deleted: ${file.originalName}`);
    }
}

// ============================================
// File List
// ============================================

function loadFiles() {
    const allFiles = getFiles();
    files = allFiles.filter(f => f.userId === currentUser.id);
    
    const filesList = document.getElementById('filesList');
    
    if (files.length === 0) {
        filesList.innerHTML = `
            <div class="empty-state">
                <div class="icon">📁</div>
                <h3>No files yet</h3>
                <p>Upload and encrypt your first file to get started</p>
            </div>
        `;
        return;
    }
    
    filesList.innerHTML = files.map(file => `
        <div class="file-item" data-file-id="${file.id}">
            <div class="file-info">
                <div class="file-name">🔒 ${file.originalName}</div>
                <div class="file-meta">
                    <span>📊 ${formatFileSize(file.size)}</span>
                    <span>🔐 ${getMethodName(file.method)}</span>
                    <span>📅 ${formatDate(file.createdAt)}</span>
                </div>
            </div>
            <div class="file-actions">
                <button class="btn btn-success" onclick="openDecryptModal('${file.id}')">
                    🔓 Decrypt
                </button>
                <button class="btn btn-primary" onclick="openShareModal('${file.id}')">
                    🔗 Share
                </button>
                <button class="btn btn-danger" onclick="deleteFile('${file.id}')">
                    🗑️ Delete
                </button>
            </div>
        </div>
    `).join('');
}

function filterFiles() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const fileItems = document.querySelectorAll('.file-item');
    
    fileItems.forEach(item => {
        const fileName = item.querySelector('.file-name').textContent.toLowerCase();
        if (fileName.includes(searchTerm)) {
            item.style.display = 'flex';
        } else {
            item.style.display = 'none';
        }
    });
}

// ============================================
// Modals
// ============================================

function openDecryptModal(fileId) {
    currentFileId = fileId;
    const file = files.find(f => f.id === fileId);
    
    document.getElementById('decryptFileName').textContent = file.originalName;
    document.getElementById('decryptPassword').value = '';
    document.getElementById('decryptExtraKey').value = '';
    document.getElementById('decryptModal').classList.add('active');
}

function closeDecryptModal() {
    document.getElementById('decryptModal').classList.remove('active');
    currentFileId = null;
}

function openShareModal(fileId) {
    currentFileId = fileId;
    const file = files.find(f => f.id === fileId);
    
    document.getElementById('shareFileName').textContent = file.originalName;
    document.getElementById('shareExpiry').value = '24';
    document.getElementById('sharePassword').value = '';
    document.getElementById('shareLinkResult').style.display = 'none';
    document.getElementById('shareModal').classList.add('active');
}

function closeShareModal() {
    document.getElementById('shareModal').classList.remove('active');
    currentFileId = null;
}

function createShareLink() {
    const expiryHours = parseInt(document.getElementById('shareExpiry').value);
    const sharePassword = document.getElementById('sharePassword').value;
    
    const shareToken = cryptoManager.generateToken(32);
    const expiresAt = new Date(Date.now() + expiryHours * 60 * 60 * 1000).toISOString();
    
    const share = {
        token: shareToken,
        fileId: currentFileId,
        userId: currentUser.id,
        password: sharePassword,
        expiresAt: expiresAt,
        createdAt: new Date().toISOString(),
        downloads: 0
    };
    
    const shares = getShares();
    shares.push(share);
    saveShares(shares);
    
    const shareUrl = `${window.location.origin}/share.html?token=${shareToken}`;
    document.getElementById('shareLinkUrl').value = shareUrl;
    document.getElementById('shareLinkResult').style.display = 'block';
    
    showAlert('Share link created successfully!', 'success');
    
    // Add audit log
    const file = files.find(f => f.id === currentFileId);
    if (file) {
        addAuditLog('share', `Created share link for: ${file.originalName}`);
        
        // Add notification
        addNotification('file_shared', 'File Shared', `Created share link for: ${file.originalName}`);
    }
}

function copyShareLink() {
    const input = document.getElementById('shareLinkUrl');
    input.select();
    document.execCommand('copy');
    showAlert('Link copied to clipboard!', 'success');
}

// ============================================
// Stats
// ============================================

function updateStats() {
    const totalFiles = files.length;
    const totalSize = files.reduce((sum, f) => sum + f.size, 0);
    const shares = getShares().filter(s => s.userId === currentUser.id);
    
    document.getElementById('totalFiles').textContent = totalFiles;
    document.getElementById('totalSize').textContent = formatFileSize(totalSize);
    document.getElementById('encryptedFiles').textContent = totalFiles;
    document.getElementById('sharedFiles').textContent = shares.length;
}

// ============================================
// LocalStorage Helpers
// ============================================

function getUsers() {
    const data = localStorage.getItem(STORAGE_KEYS.USERS);
    return data ? JSON.parse(data) : [];
}

function saveUsers(users) {
    localStorage.setItem(STORAGE_KEYS.USERS, JSON.stringify(users));
}

function getFiles() {
    const data = localStorage.getItem(STORAGE_KEYS.FILES);
    return data ? JSON.parse(data) : [];
}

function saveFiles(files) {
    localStorage.setItem(STORAGE_KEYS.FILES, JSON.stringify(files));
}

function getShares() {
    const data = localStorage.getItem(STORAGE_KEYS.SHARES);
    return data ? JSON.parse(data) : [];
}

function saveShares(shares) {
    localStorage.setItem(STORAGE_KEYS.SHARES, JSON.stringify(shares));
}

// ============================================
// Utility Functions
// ============================================

function readFileAsArrayBuffer(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsArrayBuffer(file);
    });
}

function downloadFile(data, filename) {
    const blob = new Blob([data]);
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function arrayBufferToBase64(buffer) {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    for (let i = 0; i < bytes.byteLength; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
}

function base64ToArrayBuffer(base64) {
    const binary = atob(base64);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
        bytes[i] = binary.charCodeAt(i);
    }
    return bytes.buffer;
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

function getMethodName(method) {
    const names = {
        'aes': 'AES-256-GCM',
        'chacha': 'ChaCha20-Poly1305'
    };
    return names[method] || method.toUpperCase();
}

function showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    document.body.appendChild(alert);
    
    setTimeout(() => {
        alert.remove();
    }, 3000);
}

function showLoading(message = 'Processing...') {
    const overlay = document.createElement('div');
    overlay.id = 'loadingOverlay';
    overlay.className = 'loading-overlay';
    overlay.innerHTML = `
        <div class="loading-content">
            <div class="spinner"></div>
            <p>${message}</p>
        </div>
    `;
    document.body.appendChild(overlay);
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.remove();
    }
}

// Close modals when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('active');
    }
}
