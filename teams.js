/**
 * Teams Management Module
 */

// ============================================
// Teams State
// ============================================

let teams = [];
let currentTeam = null;

// ============================================
// Page Navigation
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
    if (pageId === 'teamsPage') {
        loadTeams();
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
// Teams Functions
// ============================================

function loadTeams() {
    const allTeams = getTeams();
    teams = allTeams.filter(t => 
        t.members && t.members.some(m => m.userId === currentUser.id)
    );
    
    const teamsList = document.getElementById('teamsList');
    
    if (teams.length === 0) {
        teamsList.innerHTML = `
            <div class="empty-teams">
                <div class="icon">👥</div>
                <h3>No Teams Yet</h3>
                <p>Create your first team to collaborate with others</p>
                <button onclick="openCreateTeamModal()" class="btn btn-primary">Create Team</button>
            </div>
        `;
        return;
    }
    
    teamsList.innerHTML = teams.map(team => {
        const userMember = team.members.find(m => m.userId === currentUser.id);
        const role = userMember ? userMember.role : 'member';
        
        return `
            <div class="team-card">
                <div class="team-header">
                    <div class="team-name">${team.name}</div>
                    <div class="team-role">${role}</div>
                </div>
                <div class="team-description">${team.description || 'No description'}</div>
                <div class="team-stats">
                    <div class="team-stat">
                        <div class="team-stat-value">${team.members.length}</div>
                        <div class="team-stat-label">Members</div>
                    </div>
                    <div class="team-stat">
                        <div class="team-stat-value">${team.filesCount || 0}</div>
                        <div class="team-stat-label">Files</div>
                    </div>
                    <div class="team-stat">
                        <div class="team-stat-value">${formatDate(team.createdAt).split(' ')[0]}</div>
                        <div class="team-stat-label">Created</div>
                    </div>
                </div>
                <div class="team-actions">
                    <button class="btn btn-primary" onclick="viewTeam('${team.id}')">View</button>
                    ${role === 'admin' ? `<button class="btn btn-secondary" onclick="manageTeam('${team.id}')">Manage</button>` : ''}
                </div>
            </div>
        `;
    }).join('');
}

function openCreateTeamModal() {
    document.getElementById('teamName').value = '';
    document.getElementById('teamDescription').value = '';
    document.getElementById('createTeamModal').classList.add('active');
}

function closeCreateTeamModal() {
    document.getElementById('createTeamModal').classList.remove('active');
}

function createTeam() {
    const name = document.getElementById('teamName').value.trim();
    const description = document.getElementById('teamDescription').value.trim();
    
    if (!name) {
        showAlert('Team name is required', 'error');
        return;
    }
    
    const team = {
        id: cryptoManager.generateToken(16),
        name: name,
        description: description,
        createdBy: currentUser.id,
        createdAt: new Date().toISOString(),
        members: [
            {
                userId: currentUser.id,
                role: 'admin',
                joinedAt: new Date().toISOString()
            }
        ],
        filesCount: 0
    };
    
    const allTeams = getTeams();
    allTeams.push(team);
    saveTeams(allTeams);
    
    closeCreateTeamModal();
    loadTeams();
    showAlert('Team created successfully!', 'success');
    
    // Add notification
    addNotification('team_created', 'Team Created', `You created team: ${name}`);
}

function viewTeam(teamId) {
    currentTeam = teams.find(t => t.id === teamId);
    showAlert(`Viewing team: ${currentTeam.name}`, 'info');
    // In a full implementation, this would show team details page
}

function manageTeam(teamId) {
    currentTeam = teams.find(t => t.id === teamId);
    showAlert(`Managing team: ${currentTeam.name}`, 'info');
    // In a full implementation, this would show team management page
}

// ============================================
// LocalStorage Helpers
// ============================================

function getTeams() {
    const data = localStorage.getItem('vault_teams');
    return data ? JSON.parse(data) : [];
}

function saveTeams(teams) {
    localStorage.setItem('vault_teams', JSON.stringify(teams));
}
