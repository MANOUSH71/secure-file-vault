/**
 * Audit Logs Module
 */

// ============================================
// Audit Logs Functions
// ============================================

function loadAuditLogs() {
    displayAuditLogs();
}

function displayAuditLogs() {
    const container = document.getElementById('auditLogsList');
    if (!container) return;
    
    let logs = getAuditLogs();
    
    // Filter by user
    logs = logs.filter(log => log.userId === currentUser.id);
    
    // Apply filters
    const searchTerm = document.getElementById('auditSearch')?.value.toLowerCase() || '';
    const actionFilter = document.getElementById('auditAction')?.value || '';
    const dateFilter = document.getElementById('auditDate')?.value || '';
    
    if (searchTerm) {
        logs = logs.filter(log => 
            log.action.toLowerCase().includes(searchTerm) ||
            log.details.toLowerCase().includes(searchTerm)
        );
    }
    
    if (actionFilter) {
        logs = logs.filter(log => log.action === actionFilter);
    }
    
    if (dateFilter) {
        logs = logs.filter(log => {
            const logDate = new Date(log.timestamp).toISOString().split('T')[0];
            return logDate === dateFilter;
        });
    }
    
    // Sort by date (newest first)
    logs.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
    
    if (logs.length === 0) {
        container.innerHTML = `
            <div class="empty-logs">
                <div class="icon">📋</div>
                <h3>No Audit Logs</h3>
                <p>No activity logs found</p>
            </div>
        `;
        return;
    }
    
    // Header
    let html = `
        <div class="audit-log-item audit-log-header">
            <div>Time</div>
            <div>Action</div>
            <div>Details</div>
            <div>IP Address</div>
            <div>User Agent</div>
        </div>
    `;
    
    // Logs
    html += logs.map(log => `
        <div class="audit-log-item">
            <div class="audit-time">${formatDate(log.timestamp)}</div>
            <div class="audit-action ${log.action}">${log.action}</div>
            <div class="audit-details">${log.details}</div>
            <div class="audit-ip">${log.ipAddress || 'N/A'}</div>
            <div class="audit-ip">${log.userAgent ? log.userAgent.substring(0, 30) + '...' : 'N/A'}</div>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

function filterAuditLogs() {
    displayAuditLogs();
}

function exportAuditLogs() {
    const logs = getAuditLogs().filter(log => log.userId === currentUser.id);
    
    if (logs.length === 0) {
        showAlert('No logs to export', 'error');
        return;
    }
    
    // Create CSV
    let csv = 'Timestamp,Action,Details,IP Address,User Agent\n';
    
    logs.forEach(log => {
        csv += `"${log.timestamp}","${log.action}","${log.details}","${log.ipAddress || 'N/A'}","${log.userAgent || 'N/A'}"\n`;
    });
    
    // Download
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `audit_logs_${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showAlert('Audit logs exported successfully', 'success');
    
    // Add log
    addAuditLog('export', 'Exported audit logs');
}

function addAuditLog(action, details) {
    const log = {
        id: cryptoManager.generateToken(16),
        userId: currentUser.id,
        username: currentUser.username,
        action: action,
        details: details,
        timestamp: new Date().toISOString(),
        ipAddress: 'Local',
        userAgent: navigator.userAgent
    };
    
    const logs = getAuditLogs();
    logs.push(log);
    saveAuditLogs(logs);
}

// ============================================
// LocalStorage Helpers
// ============================================

function getAuditLogs() {
    const data = localStorage.getItem('vault_audit_logs');
    return data ? JSON.parse(data) : [];
}

function saveAuditLogs(logs) {
    localStorage.setItem('vault_audit_logs', JSON.stringify(logs));
}
