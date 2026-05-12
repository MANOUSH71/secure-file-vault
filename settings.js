/**
 * Settings Management Module
 */

// ============================================
// Settings State
// ============================================

// ============================================
// Page Navigation (Overriding app.js showPage if needed)
// ============================================

function showPage(pageId) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // Show selected page
    document.getElementById(pageId).classList.add('active');
    
    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('onclick') && link.getAttribute('onclick').includes(pageId)) {
            link.classList.add('active');
        }
    });
    
    // Update user display on all pages
    if (currentUser) {
        for (let i = 1; i <= 6; i++) {
            const userDisplay = document.getElementById(`userDisplay${i}`);
            if (userDisplay) {
                userDisplay.textContent = `${currentUser.firstName} ${currentUser.lastName}`;
            }
        }
    }
    
    // Load page data
    if (pageId === 'settingsPage') {
        loadSettings();
    } else if (pageId === 'analyticsPage') {
        loadAnalytics();
    } else if (pageId === 'notificationsPage') {
        loadNotifications();
    } else if (pageId === 'auditPage') {
        loadAuditLogs();
    } else if (pageId === 'fileRequestsPage') {
        loadFileRequests();
    }
}

// ============================================
// Settings Functions
// ============================================

function loadSettings() {
    if (!currentUser) return;
    
    document.getElementById('setFirstName').value = currentUser.firstName || '';
    document.getElementById('setLastName').value = currentUser.lastName || '';
    document.getElementById('setUsername').value = currentUser.username || '';
}

async function updateProfile(event) {
    event.preventDefault();
    
    const firstName = document.getElementById('setFirstName').value.trim();
    const lastName = document.getElementById('setLastName').value.trim();
    
    if (!firstName || !lastName) {
        showAlert('First and last name are required', 'error');
        return;
    }
    
    const users = getUsers();
    const userIndex = users.findIndex(u => u.id === currentUser.id);
    
    if (userIndex !== -1) {
        users[userIndex].firstName = firstName;
        users[userIndex].lastName = lastName;
        
        saveUsers(users);
        currentUser = users[userIndex];
        
        // Update displays
        document.getElementById('userDisplay').textContent = `${currentUser.firstName} ${currentUser.lastName}`;
        for (let i = 1; i <= 6; i++) {
            const userDisplay = document.getElementById(`userDisplay${i}`);
            if (userDisplay) {
                userDisplay.textContent = `${currentUser.firstName} ${currentUser.lastName}`;
            }
        }
        
        showAlert('Profile updated successfully!', 'success');
        addAuditLog('settings_update', 'Updated profile information');
    }
}

async function updatePassword(event) {
    event.preventDefault();
    
    const currentPass = document.getElementById('currentPassword').value;
    const newPass = document.getElementById('newPassword').value;
    const confirmPass = document.getElementById('confirmPassword').value;
    
    if (newPass !== confirmPass) {
        showAlert('New passwords do not match', 'error');
        return;
    }
    
    if (newPass.length < 8) {
        showAlert('New password must be at least 8 characters', 'error');
        return;
    }
    
    const currentHash = await cryptoManager.hashPassword(currentPass);
    
    if (currentHash !== currentUser.passwordHash) {
        showAlert('Current password is incorrect', 'error');
        return;
    }
    
    const newHash = await cryptoManager.hashPassword(newPass);
    const users = getUsers();
    const userIndex = users.findIndex(u => u.id === currentUser.id);
    
    if (userIndex !== -1) {
        users[userIndex].passwordHash = newHash;
        saveUsers(users);
        currentUser = users[userIndex];
        
        document.getElementById('currentPassword').value = '';
        document.getElementById('newPassword').value = '';
        document.getElementById('confirmPassword').value = '';
        
        showAlert('Password updated successfully!', 'success');
        addAuditLog('settings_update', 'Updated password');
    }
}

function clearAllData() {
    if (confirm('ARE YOU SURE? This will permanently delete all your encrypted files and data. This action cannot be undone!')) {
        const allFiles = getFiles();
        const otherFiles = allFiles.filter(f => f.userId !== currentUser.id);
        saveFiles(otherFiles);
        
        const allShares = getShares();
        const otherShares = allShares.filter(s => s.userId !== currentUser.id);
        saveShares(otherShares);
        
        // Clear notifications and audit logs if they are user-specific
        // (Assuming they are filtered by userId in their respective modules)
        
        showAlert('All your data has been cleared.', 'info');
        addAuditLog('settings_clear', 'Cleared all user data');
        
        showPage('dashboardPage');
        loadFiles();
        updateStats();
    }
}

// ============================================
// LocalStorage Helpers (Re-using from app.js if possible)
// ============================================

function saveUsers(users) {
    localStorage.setItem('vault_users', JSON.stringify(users));
}

function getFiles() {
    const data = localStorage.getItem('vault_files');
    return data ? JSON.parse(data) : [];
}

function saveFiles(files) {
    localStorage.setItem('vault_files', JSON.stringify(files));
}

function getShares() {
    const data = localStorage.getItem('vault_shares');
    return data ? JSON.parse(data) : [];
}

function saveShares(shares) {
    localStorage.setItem('vault_shares', JSON.stringify(shares));
}
