/**
 * File Requests Module
 */

// ============================================
// File Requests Functions
// ============================================

function loadFileRequests() {
    const allRequests = getFileRequests();
    const requests = allRequests.filter(r => r.userId === currentUser.id);
    
    const container = document.getElementById('fileRequestsList');
    if (!container) return;
    
    if (requests.length === 0) {
        container.innerHTML = `
            <div class="empty-requests">
                <div class="icon">📥</div>
                <h3>No File Requests</h3>
                <p>Create a request to receive files from others</p>
                <button onclick="openCreateRequestModal()" class="btn btn-primary">Create Request</button>
            </div>
        `;
        return;
    }
    
    // Sort by date (newest first)
    requests.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    
    container.innerHTML = requests.map(request => {
        const isExpired = new Date(request.expiresAt) < new Date();
        const status = isExpired ? 'expired' : 'active';
        const statusText = isExpired ? 'Expired' : 'Active';
        
        return `
            <div class="request-card">
                <div class="request-header">
                    <div class="request-title">${request.title}</div>
                    <div class="request-status ${status}">${statusText}</div>
                </div>
                
                <div class="request-info">
                    <div class="request-info-item">
                        <div class="request-info-value">${request.filesReceived || 0}</div>
                        <div class="request-info-label">Received</div>
                    </div>
                    <div class="request-info-item">
                        <div class="request-info-value">${request.maxFiles}</div>
                        <div class="request-info-label">Max Files</div>
                    </div>
                    <div class="request-info-item">
                        <div class="request-info-value">${getTimeRemaining(request.expiresAt)}</div>
                        <div class="request-info-label">Time Left</div>
                    </div>
                </div>
                
                <div class="request-link">
                    ${window.location.origin}/upload.html?token=${request.token}
                </div>
                
                <div class="request-actions">
                    <button class="btn btn-primary" onclick="copyRequestLinkDirect('${request.token}')">📋 Copy Link</button>
                    ${!isExpired ? `<button class="btn btn-secondary" onclick="extendRequest('${request.id}')">⏰ Extend</button>` : ''}
                    <button class="btn btn-danger" onclick="deleteRequest('${request.id}')">🗑️ Delete</button>
                </div>
            </div>
        `;
    }).join('');
}

function openCreateRequestModal() {
    document.getElementById('requestTitle').value = '';
    document.getElementById('requestMaxFiles').value = '5';
    document.getElementById('requestExpiry').value = '48';
    document.getElementById('requestLinkResult').style.display = 'none';
    document.getElementById('createRequestModal').classList.add('active');
}

function closeCreateRequestModal() {
    document.getElementById('createRequestModal').classList.remove('active');
}

function createFileRequest() {
    const title = document.getElementById('requestTitle').value.trim();
    const maxFiles = parseInt(document.getElementById('requestMaxFiles').value);
    const expiryHours = parseInt(document.getElementById('requestExpiry').value);
    
    if (!title) {
        showAlert('Request title is required', 'error');
        return;
    }
    
    const token = cryptoManager.generateToken(32);
    const expiresAt = new Date(Date.now() + expiryHours * 60 * 60 * 1000).toISOString();
    
    const request = {
        id: cryptoManager.generateToken(16),
        userId: currentUser.id,
        token: token,
        title: title,
        maxFiles: maxFiles,
        filesReceived: 0,
        expiresAt: expiresAt,
        createdAt: new Date().toISOString()
    };
    
    const allRequests = getFileRequests();
    allRequests.push(request);
    saveFileRequests(allRequests);
    
    // Show link
    const requestUrl = `${window.location.origin}/upload.html?token=${token}`;
    document.getElementById('requestLinkUrl').value = requestUrl;
    document.getElementById('requestLinkResult').style.display = 'block';
    
    showAlert('File request created successfully!', 'success');
    
    // Add notification
    addNotification('file_request_created', 'File Request Created', `Created request: ${title}`);
    
    // Add audit log
    addAuditLog('create_request', `Created file request: ${title}`);
}

function copyRequestLink() {
    const input = document.getElementById('requestLinkUrl');
    input.select();
    document.execCommand('copy');
    showAlert('Link copied to clipboard!', 'success');
}

function copyRequestLinkDirect(token) {
    const url = `${window.location.origin}/upload.html?token=${token}`;
    
    // Create temporary input
    const input = document.createElement('input');
    input.value = url;
    document.body.appendChild(input);
    input.select();
    document.execCommand('copy');
    document.body.removeChild(input);
    
    showAlert('Link copied to clipboard!', 'success');
}

function extendRequest(requestId) {
    const allRequests = getFileRequests();
    const request = allRequests.find(r => r.id === requestId);
    
    if (request) {
        // Extend by 24 hours
        const currentExpiry = new Date(request.expiresAt);
        currentExpiry.setHours(currentExpiry.getHours() + 24);
        request.expiresAt = currentExpiry.toISOString();
        
        saveFileRequests(allRequests);
        loadFileRequests();
        showAlert('Request extended by 24 hours', 'success');
        
        // Add audit log
        addAuditLog('extend_request', `Extended file request: ${request.title}`);
    }
}

function deleteRequest(requestId) {
    if (!confirm('Are you sure you want to delete this request?')) {
        return;
    }
    
    const allRequests = getFileRequests();
    const request = allRequests.find(r => r.id === requestId);
    const filtered = allRequests.filter(r => r.id !== requestId);
    
    saveFileRequests(filtered);
    loadFileRequests();
    showAlert('Request deleted successfully', 'success');
    
    // Add audit log
    if (request) {
        addAuditLog('delete_request', `Deleted file request: ${request.title}`);
    }
}

// ============================================
// Helper Functions
// ============================================

function getTimeRemaining(expiresAt) {
    const now = new Date();
    const expiry = new Date(expiresAt);
    const diff = expiry - now;
    
    if (diff <= 0) return 'Expired';
    
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(hours / 24);
    
    if (days > 0) return `${days}d`;
    if (hours > 0) return `${hours}h`;
    return '< 1h';
}

// ============================================
// LocalStorage Helpers
// ============================================

function getFileRequests() {
    const data = localStorage.getItem('vault_file_requests');
    return data ? JSON.parse(data) : [];
}

function saveFileRequests(requests) {
    localStorage.setItem('vault_file_requests', JSON.stringify(requests));
}
