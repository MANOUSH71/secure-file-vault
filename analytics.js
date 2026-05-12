/**
 * Analytics Module
 */

// ============================================
// Analytics Functions
// ============================================

function loadAnalytics() {
    loadActivityChart();
    loadMethodsChart();
    loadSizeDistribution();
    loadTopShared();
}

function loadActivityChart() {
    const canvas = document.getElementById('activityChart');
    if (!canvas) return;
    
    // Simple text-based chart (in production, use Chart.js)
    const ctx = canvas.getContext('2d');
    canvas.width = canvas.offsetWidth;
    canvas.height = 200;
    
    // Get activity data
    const logs = getAuditLogs();
    const last7Days = getLast7Days();
    const activityData = last7Days.map(date => {
        return logs.filter(log => {
            const logDate = new Date(log.timestamp).toDateString();
            return logDate === date.toDateString();
        }).length;
    });
    
    // Draw simple bar chart
    ctx.fillStyle = '#6366f1';
    const barWidth = canvas.width / 7;
    const maxValue = Math.max(...activityData, 1);
    
    activityData.forEach((value, index) => {
        const barHeight = (value / maxValue) * 150;
        const x = index * barWidth + 10;
        const y = canvas.height - barHeight - 20;
        
        ctx.fillRect(x, y, barWidth - 20, barHeight);
        
        // Draw value
        ctx.fillStyle = '#1e293b';
        ctx.font = '12px Arial';
        ctx.fillText(value, x + (barWidth - 20) / 2 - 5, y - 5);
        ctx.fillStyle = '#6366f1';
    });
    
    // Draw labels
    ctx.fillStyle = '#64748b';
    ctx.font = '10px Arial';
    last7Days.forEach((date, index) => {
        const x = index * barWidth + 10;
        const label = date.toLocaleDateString('en-US', { weekday: 'short' });
        ctx.fillText(label, x, canvas.height - 5);
    });
}

function loadMethodsChart() {
    const canvas = document.getElementById('methodsChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    canvas.width = canvas.offsetWidth;
    canvas.height = 200;
    
    // Get encryption methods distribution
    const allFiles = getFiles();
    const userFiles = allFiles.filter(f => f.userId === currentUser.id);
    
    const methods = {
        'aes': 0,
        'chacha': 0
    };
    
    userFiles.forEach(file => {
        if (methods.hasOwnProperty(file.method)) {
            methods[file.method]++;
        }
    });
    
    // Draw pie chart
    const total = Object.values(methods).reduce((a, b) => a + b, 0);
    if (total === 0) {
        ctx.fillStyle = '#64748b';
        ctx.font = '14px Arial';
        ctx.fillText('No data available', canvas.width / 2 - 60, canvas.height / 2);
        return;
    }
    
    const colors = {
        'aes': '#6366f1',
        'chacha': '#8b5cf6'
    };
    
    let currentAngle = 0;
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 70;
    
    Object.entries(methods).forEach(([method, count]) => {
        const sliceAngle = (count / total) * 2 * Math.PI;
        
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
        ctx.closePath();
        ctx.fillStyle = colors[method];
        ctx.fill();
        
        // Draw label
        const labelAngle = currentAngle + sliceAngle / 2;
        const labelX = centerX + Math.cos(labelAngle) * (radius + 30);
        const labelY = centerY + Math.sin(labelAngle) * (radius + 30);
        
        ctx.fillStyle = '#1e293b';
        ctx.font = '12px Arial';
        ctx.fillText(`${method.toUpperCase()}: ${count}`, labelX - 20, labelY);
        
        currentAngle += sliceAngle;
    });
}

function loadSizeDistribution() {
    const container = document.getElementById('sizeDistribution');
    if (!container) return;
    
    const allFiles = getFiles();
    const userFiles = allFiles.filter(f => f.userId === currentUser.id);
    
    const ranges = {
        '< 1 MB': 0,
        '1-10 MB': 0,
        '10-50 MB': 0,
        '> 50 MB': 0
    };
    
    userFiles.forEach(file => {
        const sizeMB = file.size / (1024 * 1024);
        if (sizeMB < 1) ranges['< 1 MB']++;
        else if (sizeMB < 10) ranges['1-10 MB']++;
        else if (sizeMB < 50) ranges['10-50 MB']++;
        else ranges['> 50 MB']++;
    });
    
    const total = userFiles.length || 1;
    
    container.innerHTML = Object.entries(ranges).map(([range, count]) => {
        const percentage = (count / total) * 100;
        return `
            <div class="distribution-item">
                <div>
                    <strong>${range}</strong>
                    <div class="distribution-bar" style="width: ${percentage}%; max-width: 200px;"></div>
                </div>
                <span>${count} files (${percentage.toFixed(1)}%)</span>
            </div>
        `;
    }).join('');
}

function loadTopShared() {
    const container = document.getElementById('topShared');
    if (!container) return;
    
    const shares = getShares().filter(s => s.userId === currentUser.id);
    const allFiles = getFiles();
    
    // Count shares per file
    const fileShares = {};
    shares.forEach(share => {
        fileShares[share.fileId] = (fileShares[share.fileId] || 0) + 1;
    });
    
    // Get top 5
    const topFiles = Object.entries(fileShares)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)
        .map(([fileId, count]) => {
            const file = allFiles.find(f => f.id === fileId);
            return { file, count };
        })
        .filter(item => item.file);
    
    if (topFiles.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #64748b;">No shared files yet</p>';
        return;
    }
    
    container.innerHTML = topFiles.map(({ file, count }) => `
        <div class="shared-item">
            <div>
                <strong>${file.originalName}</strong>
                <div style="font-size: 0.85rem; color: #64748b;">${formatFileSize(file.size)}</div>
            </div>
            <div style="text-align: right;">
                <strong style="color: #6366f1;">${count}</strong>
                <div style="font-size: 0.85rem; color: #64748b;">shares</div>
            </div>
        </div>
    `).join('');
}

// ============================================
// Helper Functions
// ============================================

function getLast7Days() {
    const days = [];
    for (let i = 6; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        days.push(date);
    }
    return days;
}
