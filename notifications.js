/**
 * Notifications Module
 */

// ============================================
// Notifications State
// ============================================

let notifications = [];
let currentFilter = 'all';

// ============================================
// Notifications Functions
// ============================================

function loadNotifications() {
    const allNotifications = getNotifications();
    notifications = allNotifications.filter(n => n.userId === currentUser.id);
    
    // Update badge
    const unreadCount = notifications.filter(n => !n.read).length;
    const badge = document.getElementById('notifBadge');
    if (badge) {
        badge.textContent = unreadCount;
        badge.style.display = unreadCount > 0 ? 'inline' : 'none';
    }
    
    displayNotifications();
}

function displayNotifications() {
    const container = document.getElementById('notificationsList');
    if (!container) return;
    
    let filtered = notifications;
    
    // Apply filter
    if (currentFilter === 'unread') {
        filtered = notifications.filter(n => !n.read);
    } else if (currentFilter !== 'all') {
        filtered = notifications.filter(n => n.type === currentFilter);
    }
    
    // Sort by date (newest first)
    filtered.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    
    if (filtered.length === 0) {
        container.innerHTML = `
            <div class="empty-notifications">
                <div class="icon">🔔</div>
                <h3>No Notifications</h3>
                <p>You're all caught up!</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = filtered.map(notif => {
        const icon = getNotificationIcon(notif.type);
        const unreadClass = notif.read ? '' : 'unread';
        
        return `
            <div class="notification-item ${unreadClass}" data-id="${notif.id}">
                <div class="notification-icon">${icon}</div>
                <div class="notification-content">
                    <div class="notification-title">${notif.title}</div>
                    <div class="notification-message">${notif.message}</div>
                    <div class="notification-time">${getTimeAgo(notif.createdAt)}</div>
                </div>
                <div class="notification-actions">
                    ${!notif.read ? `<button class="btn btn-primary" onclick="markNotificationRead('${notif.id}')">Mark Read</button>` : ''}
                    <button class="btn btn-danger" onclick="deleteNotification('${notif.id}')">Delete</button>
                </div>
            </div>
        `;
    }).join('');
}

function filterNotifications(filter) {
    currentFilter = filter;
    
    // Update active button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    displayNotifications();
}

function markNotificationRead(notifId) {
    const allNotifications = getNotifications();
    const notif = allNotifications.find(n => n.id === notifId);
    if (notif) {
        notif.read = true;
        saveNotifications(allNotifications);
        loadNotifications();
        showAlert('Notification marked as read', 'success');
    }
}

function markAllNotificationsRead() {
    const allNotifications = getNotifications();
    allNotifications.forEach(n => {
        if (n.userId === currentUser.id) {
            n.read = true;
        }
    });
    saveNotifications(allNotifications);
    loadNotifications();
    showAlert('All notifications marked as read', 'success');
}

function deleteNotification(notifId) {
    const allNotifications = getNotifications();
    const filtered = allNotifications.filter(n => n.id !== notifId);
    saveNotifications(filtered);
    loadNotifications();
    showAlert('Notification deleted', 'success');
}

function addNotification(type, title, message, link = null) {
    const notification = {
        id: cryptoManager.generateToken(16),
        userId: currentUser.id,
        type: type,
        title: title,
        message: message,
        link: link,
        read: false,
        createdAt: new Date().toISOString()
    };
    
    const allNotifications = getNotifications();
    allNotifications.push(notification);
    saveNotifications(allNotifications);
    
    // Update badge if on notifications page
    if (document.getElementById('notificationsPage').classList.contains('active')) {
        loadNotifications();
    }
}

// ============================================
// Helper Functions
// ============================================

function getNotificationIcon(type) {
    const icons = {
        'file_encrypted': '🔒',
        'file_decrypted': '🔓',
        'file_shared': '🔗',
        'file_deleted': '🗑️',
        'team_created': '👥',
        'team_joined': '✅',
        'team_left': '👋',
        'file_uploaded': '📤',
        'file_downloaded': '📥',
        'share_accessed': '👁️',
        'default': '🔔'
    };
    return icons[type] || icons['default'];
}

function getTimeAgo(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);
    
    if (seconds < 60) return 'Just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)} minutes ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`;
    if (seconds < 604800) return `${Math.floor(seconds / 86400)} days ago`;
    return date.toLocaleDateString();
}

// ============================================
// LocalStorage Helpers
// ============================================

function getNotifications() {
    const data = localStorage.getItem('vault_notifications');
    return data ? JSON.parse(data) : [];
}

function saveNotifications(notifications) {
    localStorage.setItem('vault_notifications', JSON.stringify(notifications));
}
