#!/usr/bin/env python3
"""
Secure File Vault Pro - Web Application
Flask Backend with Multiple Encryption Methods
"""

from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
from datetime import datetime, timedelta
from pathlib import Path
import json
import io
import csv

from crypto_manager import CryptoManager
from models import Database

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

CORS(app)

# Initialize
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
db = Database()
crypto = CryptoManager()


# ─────────────────────────────────────────────────────────────
# AUTH ROUTES
# ─────────────────────────────────────────────────────────────
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    first_name = data.get('first_name', '').strip()
    last_name = data.get('last_name', '').strip()
    
    if not all([username, password, first_name, last_name]):
        return jsonify({'error': 'All fields required'}), 400
    
    if db.get_user_by_username(username):
        return jsonify({'error': 'Username already exists'}), 400
    
    user_id = db.create_user(username, password, first_name, last_name)
    session['user_id'] = user_id
    session['username'] = username
    session.permanent = True
    
    return jsonify({'success': True, 'message': 'Account created successfully'})


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    user = db.get_user_by_username(username)
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    session['user_id'] = user['id']
    session['username'] = user['username']
    session.permanent = True
    
    return jsonify({'success': True, 'message': 'Login successful'})


@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})


# ─────────────────────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────────────────────
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user = db.get_user_by_id(session['user_id'])
    files = db.get_user_files(session['user_id'])
    
    return render_template('dashboard_english.html', 
                         user=user, 
                         files=files,
                         encryption_methods=crypto.get_available_methods())


# ─────────────────────────────────────────────────────────────
# FILE OPERATIONS
# ─────────────────────────────────────────────────────────────
@app.route('/api/encrypt', methods=['POST'])
def encrypt_file():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    password = request.form.get('password')
    extra_key = request.form.get('extra_key', '')
    method = request.form.get('method', 'aes')
    
    if not password:
        return jsonify({'error': 'Password required'}), 400
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Read file data
        file_data = file.read()
        original_size = len(file_data)
        
        # Encrypt
        encrypted_data = crypto.encrypt(file_data, password, extra_key, method)
        
        # Save encrypted file
        file_id = secrets.token_hex(16)
        encrypted_filename = f"{file_id}.enc"
        encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], encrypted_filename)
        
        with open(encrypted_path, 'wb') as f:
            f.write(encrypted_data)
        
        # Save to database
        db.add_file(
            user_id=session['user_id'],
            file_id=file_id,
            original_name=secure_filename(file.filename),
            encrypted_name=encrypted_filename,
            size=original_size,
            encryption_method=method
        )
        
        return jsonify({
            'success': True,
            'file_id': file_id,
            'message': 'File encrypted successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/decrypt/<file_id>', methods=['POST'])
def decrypt_file(file_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    password = data.get('password')
    extra_key = data.get('extra_key', '')
    
    if not password:
        return jsonify({'error': 'Password required'}), 400
    
    # Get file info
    file_info = db.get_file(file_id, session['user_id'])
    if not file_info:
        return jsonify({'error': 'File not found'}), 404
    
    try:
        # Read encrypted file
        encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], file_info['encrypted_name'])
        with open(encrypted_path, 'rb') as f:
            encrypted_data = f.read()
        
        # Decrypt
        decrypted_data = crypto.decrypt(
            encrypted_data, 
            password, 
            extra_key, 
            file_info['encryption_method']
        )
        
        # Save temporarily
        temp_id = secrets.token_hex(8)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_{temp_id}_{file_info['original_name']}")
        
        with open(temp_path, 'wb') as f:
            f.write(decrypted_data)
        
        return jsonify({
            'success': True,
            'temp_file': f"temp_{temp_id}_{file_info['original_name']}",
            'original_name': file_info['original_name']
        })
        
    except Exception as e:
        return jsonify({'error': f'Decryption failed: {str(e)}'}), 500


@app.route('/api/download/<filename>')
def download_file(filename):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        return send_file(file_path, as_attachment=True, download_name=filename.replace('temp_', '').split('_', 1)[1])
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@app.route('/api/files')
def get_files():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    files = db.get_user_files(session['user_id'])
    return jsonify({'files': files})


@app.route('/api/files/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    file_info = db.get_file(file_id, session['user_id'])
    if not file_info:
        return jsonify({'error': 'File not found'}), 404
    
    try:
        # Delete physical file
        encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], file_info['encrypted_name'])
        if os.path.exists(encrypted_path):
            os.remove(encrypted_path)
        
        # Delete from database
        db.delete_file(file_id, session['user_id'])
        
        return jsonify({'success': True, 'message': 'File deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ─────────────────────────────────────────────────────────────
# SHARING
# ─────────────────────────────────────────────────────────────
@app.route('/api/share/<file_id>', methods=['POST'])
def create_share_link(file_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    expires_hours = data.get('expires_hours', 24)
    share_password = data.get('share_password', '')
    
    file_info = db.get_file(file_id, session['user_id'])
    if not file_info:
        return jsonify({'error': 'File not found'}), 404
    
    share_token = secrets.token_urlsafe(32)
    expires_at = datetime.now() + timedelta(hours=expires_hours)
    
    db.create_share_link(file_id, share_token, expires_at, share_password)
    
    share_url = f"{request.host_url}share/{share_token}"
    
    return jsonify({
        'success': True,
        'share_url': share_url,
        'expires_at': expires_at.isoformat()
    })


@app.route('/share/<token>')
def view_shared_file(token):
    share_info = db.get_share_link(token)
    
    if not share_info:
        return render_template('error.html', message='Invalid or expired link'), 404
    
    if share_info['expires_at'] < datetime.now():
        return render_template('error.html', message='Link has expired'), 410
    
    return render_template('share.html', share_info=share_info)


@app.route('/api/share/download/<token>', methods=['POST'])
def download_shared_file(token):
    data = request.json
    share_password = data.get('share_password', '')
    
    share_info = db.get_share_link(token)
    
    if not share_info or share_info['expires_at'] < datetime.now():
        return jsonify({'error': 'Invalid or expired link'}), 404
    
    if share_info['share_password'] and share_info['share_password'] != share_password:
        return jsonify({'error': 'Invalid password'}), 401
    
    file_info = db.get_file_by_id(share_info['file_id'])
    
    try:
        encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], file_info['encrypted_name'])
        
        # Track download
        db.track_share_access(token)
        
        return send_file(
            encrypted_path, 
            as_attachment=True, 
            download_name=f"{file_info['original_name']}.encrypted"
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ─────────────────────────────────────────────────────────────
# EMAIL SENDING
# ─────────────────────────────────────────────────────────────
@app.route('/api/send-email/<file_id>', methods=['POST'])
def send_file_email(file_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    recipient_email = data.get('email')
    message = data.get('message', '')
    
    if not recipient_email:
        return jsonify({'error': 'Email required'}), 400
    
    # Create share link first
    share_token = secrets.token_urlsafe(32)
    expires_at = datetime.now() + timedelta(hours=48)
    
    db.create_share_link(file_id, share_token, expires_at, '')
    
    share_url = f"{request.host_url}share/{share_token}"
    
    # TODO: Implement actual email sending with SMTP
    # For now, just return the link
    
    return jsonify({
        'success': True,
        'message': 'Share link created (Email sending not configured yet)',
        'share_url': share_url
    })


# ─────────────────────────────────────────────────────────────
# STATS
# ─────────────────────────────────────────────────────────────
@app.route('/api/stats')
def get_stats():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    stats = db.get_user_stats(session['user_id'])
    return jsonify(stats)


# ─────────────────────────────────────────────────────────────
# TEAM MANAGEMENT (Feature 1)
# ─────────────────────────────────────────────────────────────
@app.route('/team')
def team_page():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user = db.get_user_by_id(session['user_id'])
    teams = db.get_user_teams(session['user_id'])
    
    return render_template('team.html', user=user, teams=teams)


@app.route('/api/team/create', methods=['POST'])
def create_team():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    team_name = data.get('name', '').strip()
    
    if not team_name:
        return jsonify({'error': 'Team name required'}), 400
    
    team_id = db.create_team(team_name, session['user_id'])
    
    return jsonify({'success': True, 'team_id': team_id})


@app.route('/api/team/<int:team_id>/members')
def get_team_members(team_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Verify user is team member
    membership = db.is_team_member(team_id, session['user_id'])
    if not membership:
        return jsonify({'error': 'Not a team member'}), 403
    
    members = db.get_team_members(team_id)
    return jsonify({'members': members})


@app.route('/api/team/<int:team_id>/member/<int:user_id>/role', methods=['PUT'])
def update_member_role(team_id, user_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Verify user is admin
    membership = db.is_team_member(team_id, session['user_id'])
    if not membership or membership['role'] != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    data = request.json
    new_role = data.get('role')
    
    if new_role not in ['admin', 'editor', 'viewer']:
        return jsonify({'error': 'Invalid role'}), 400
    
    db.update_member_role(team_id, user_id, new_role)
    
    return jsonify({'success': True})


@app.route('/api/team/<int:team_id>/member/<int:user_id>', methods=['DELETE'])
def remove_team_member(team_id, user_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Verify user is admin
    membership = db.is_team_member(team_id, session['user_id'])
    if not membership or membership['role'] != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    db.remove_team_member(team_id, user_id)
    
    return jsonify({'success': True})


# ─────────────────────────────────────────────────────────────
# INVITATIONS (Feature 3)
# ─────────────────────────────────────────────────────────────
@app.route('/api/team/<int:team_id>/invite', methods=['POST'])
def create_invitation(team_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Verify user is admin
    membership = db.is_team_member(team_id, session['user_id'])
    if not membership or membership['role'] != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    data = request.json
    email = data.get('email', '')
    
    token = db.create_invitation(team_id, session['user_id'], email)
    invite_url = f"{request.host_url}invite/{token}"
    
    return jsonify({'success': True, 'invite_url': invite_url, 'token': token})


@app.route('/invite/<token>')
def view_invitation(token):
    invitation = db.get_invitation(token)
    
    if not invitation:
        return render_template('error.html', message='Invalid or expired invitation'), 404
    
    if invitation['expires_at'] < datetime.now():
        return render_template('error.html', message='Invitation has expired'), 410
    
    return render_template('invitation.html', invitation=invitation)


@app.route('/api/invite/<token>/accept', methods=['POST'])
def accept_invitation(token):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    invitation = db.get_invitation(token)
    
    if not invitation or invitation['expires_at'] < datetime.now():
        return jsonify({'error': 'Invalid or expired invitation'}), 404
    
    success = db.use_invitation(token, session['user_id'])
    
    if success:
        # Create notification
        db.create_notification(
            session['user_id'],
            'team_join',
            'Joined Team',
            f"You have joined the team: {invitation['team_name']}",
            f"/team"
        )
        return jsonify({'success': True, 'team_id': invitation['team_id']})
    
    return jsonify({'error': 'Failed to accept invitation'}), 500


# ─────────────────────────────────────────────────────────────
# TEAM ACTIVITY FEED (Feature 4)
# ─────────────────────────────────────────────────────────────
@app.route('/team/<int:team_id>/activity')
def team_activity_page(team_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    # Verify user is team member
    membership = db.is_team_member(team_id, session['user_id'])
    if not membership:
        return redirect(url_for('dashboard'))
    
    user = db.get_user_by_id(session['user_id'])
    team = db.get_team(team_id)
    
    return render_template('team_activity.html', user=user, team=team)


@app.route('/api/team/<int:team_id>/activity')
def get_team_activity(team_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Verify user is team member
    membership = db.is_team_member(team_id, session['user_id'])
    if not membership:
        return jsonify({'error': 'Not a team member'}), 403
    
    activity = db.get_team_activity(team_id)
    return jsonify({'activity': activity})


# ─────────────────────────────────────────────────────────────
# ADMIN PANEL (Feature 5)
# ─────────────────────────────────────────────────────────────
@app.route('/admin/<int:team_id>')
def admin_panel(team_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    # Verify user is admin
    membership = db.is_team_member(team_id, session['user_id'])
    if not membership or membership['role'] != 'admin':
        return redirect(url_for('dashboard'))
    
    user = db.get_user_by_id(session['user_id'])
    team = db.get_team(team_id)
    members = db.get_team_members(team_id)
    
    return render_template('admin.html', user=user, team=team, members=members)


@app.route('/api/admin/<int:team_id>/user/<int:user_id>/deactivate', methods=['POST'])
def deactivate_user_admin(team_id, user_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Verify user is admin
    membership = db.is_team_member(team_id, session['user_id'])
    if not membership or membership['role'] != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    db.deactivate_user(user_id)
    
    return jsonify({'success': True})


@app.route('/api/admin/<int:team_id>/revoke-links/<int:user_id>', methods=['POST'])
def revoke_user_links(team_id, user_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Verify user is admin
    membership = db.is_team_member(team_id, session['user_id'])
    if not membership or membership['role'] != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    db.revoke_all_share_links(user_id)
    
    return jsonify({'success': True})


@app.route('/api/admin/<int:team_id>/export-audit')
def export_audit_csv(team_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Verify user is admin
    membership = db.is_team_member(team_id, session['user_id'])
    if not membership or membership['role'] != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    import csv
    import io
    
    logs = db.get_audit_logs()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Timestamp', 'User', 'Action', 'Entity Type', 'Entity ID', 'IP Address'])
    
    for log in logs:
        writer.writerow([
            log['created_at'],
            log['username'],
            log['action'],
            log['entity_type'],
            log['entity_id'],
            log['ip_address']
        ])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'audit_log_{datetime.now().strftime("%Y%m%d")}.csv'
    )


# ─────────────────────────────────────────────────────────────
# ANALYTICS (Feature 6)
# ─────────────────────────────────────────────────────────────
@app.route('/analytics/<int:team_id>')
def analytics_page(team_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    # Verify user is team member
    membership = db.is_team_member(team_id, session['user_id'])
    if not membership:
        return redirect(url_for('dashboard'))
    
    user = db.get_user_by_id(session['user_id'])
    team = db.get_team(team_id)
    
    return render_template('analytics.html', user=user, team=team)


@app.route('/api/analytics/<int:team_id>')
def get_analytics(team_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Verify user is team member
    membership = db.is_team_member(team_id, session['user_id'])
    if not membership:
        return jsonify({'error': 'Not a team member'}), 403
    
    analytics = db.get_team_analytics(team_id)
    return jsonify(analytics)


# ─────────────────────────────────────────────────────────────
# FILE REQUESTS (Feature 7)
# ─────────────────────────────────────────────────────────────
@app.route('/request')
def file_request_page():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user = db.get_user_by_id(session['user_id'])
    
    return render_template('file_request.html', user=user)


@app.route('/api/request/create', methods=['POST'])
def create_file_request():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    max_files = data.get('max_files', 1)
    expires_hours = data.get('expires_hours', 48)
    
    token = db.create_file_request(session['user_id'], None, max_files, expires_hours)
    request_url = f"{request.host_url}upload/{token}"
    
    return jsonify({'success': True, 'request_url': request_url, 'token': token})


@app.route('/upload/<token>')
def upload_page(token):
    file_request = db.get_file_request(token)
    
    if not file_request:
        return render_template('error.html', message='Invalid or expired request'), 404
    
    if file_request['expires_at'] < datetime.now():
        return render_template('error.html', message='Request has expired'), 410
    
    if file_request['files_uploaded'] >= file_request['max_files']:
        return render_template('error.html', message='Maximum files reached'), 410
    
    return render_template('upload.html', file_request=file_request)


@app.route('/api/upload/<token>', methods=['POST'])
def upload_to_request(token):
    file_request = db.get_file_request(token)
    
    if not file_request or file_request['expires_at'] < datetime.now():
        return jsonify({'error': 'Invalid or expired request'}), 404
    
    if file_request['files_uploaded'] >= file_request['max_files']:
        return jsonify({'error': 'Maximum files reached'}), 400
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    password = request.form.get('password', secrets.token_hex(16))
    
    try:
        # Read and encrypt file
        file_data = file.read()
        encrypted_data = crypto.encrypt(file_data, password, '', 'aes')
        
        # Save encrypted file
        file_id = secrets.token_hex(16)
        encrypted_filename = f"{file_id}.enc"
        encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], encrypted_filename)
        
        with open(encrypted_path, 'wb') as f:
            f.write(encrypted_data)
        
        # Save to database
        db.add_file(
            user_id=file_request['requested_by'],
            file_id=file_id,
            original_name=secure_filename(file.filename),
            encrypted_name=encrypted_filename,
            size=len(file_data),
            encryption_method='aes'
        )
        
        # Increment counter
        db.increment_file_request_count(token)
        
        # Notify requester
        db.create_notification(
            file_request['requested_by'],
            'file_uploaded',
            'File Uploaded',
            f"Someone uploaded a file: {file.filename}",
            '/dashboard'
        )
        
        return jsonify({'success': True, 'message': 'File uploaded successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ─────────────────────────────────────────────────────────────
# AUDIT LOG (Feature 8)
# ─────────────────────────────────────────────────────────────
@app.route('/audit')
def audit_page():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user = db.get_user_by_id(session['user_id'])
    
    return render_template('audit.html', user=user)


@app.route('/api/audit')
def get_audit_logs():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    logs = db.get_audit_logs(limit=limit, offset=offset)
    return jsonify({'logs': logs})


# ─────────────────────────────────────────────────────────────
# ADVANCED SEARCH (Feature 12)
# ─────────────────────────────────────────────────────────────
@app.route('/api/search')
def search_files():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    query = request.args.get('q', '')
    tag = request.args.get('tag', '')
    method = request.args.get('method', '')
    date_from = request.args.get('from', '')
    date_to = request.args.get('to', '')
    
    files = db.search_files(session['user_id'], query, tag, method, date_from, date_to)
    return jsonify({'files': files})


@app.route('/api/files/<file_id>/tags', methods=['POST'])
def add_file_tag(file_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    tag_name = data.get('tag', '').strip()
    
    if not tag_name:
        return jsonify({'error': 'Tag name required'}), 400
    
    db.add_file_tag(file_id, tag_name)
    
    return jsonify({'success': True})


# ─────────────────────────────────────────────────────────────
# NOTIFICATIONS (Feature 14)
# ─────────────────────────────────────────────────────────────
@app.route('/notifications')
def notifications_page():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user = db.get_user_by_id(session['user_id'])
    
    return render_template('notifications.html', user=user)


@app.route('/api/notifications')
def get_notifications():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    unread_only = request.args.get('unread', 'false').lower() == 'true'
    
    notifications = db.get_user_notifications(session['user_id'], unread_only)
    unread_count = db.get_unread_count(session['user_id'])
    
    return jsonify({'notifications': notifications, 'unread_count': unread_count})


@app.route('/api/notifications/<int:notification_id>/read', methods=['POST'])
def mark_notification_read(notification_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    db.mark_notification_read(notification_id)
    
    return jsonify({'success': True})


@app.route('/api/notifications/read-all', methods=['POST'])
def mark_all_notifications_read():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    db.mark_all_notifications_read(session['user_id'])
    
    return jsonify({'success': True})


# ─────────────────────────────────────────────────────────────
# SETTINGS & PROFILE (Feature 15)
# ─────────────────────────────────────────────────────────────
@app.route('/settings')
def settings_page():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user = db.get_user_by_id(session['user_id'])
    sessions = db.get_user_sessions(session['user_id'])
    
    return render_template('settings.html', user=user, sessions=sessions)


@app.route('/api/settings/profile', methods=['PUT'])
def update_profile():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    
    db.update_user_profile(
        session['user_id'],
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        preferred_language=data.get('preferred_language')
    )
    
    return jsonify({'success': True})


@app.route('/api/settings/password', methods=['PUT'])
def update_password():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    user = db.get_user_by_id(session['user_id'])
    
    if not check_password_hash(user['password'], current_password):
        return jsonify({'error': 'Current password incorrect'}), 401
    
    db.update_user_password(session['user_id'], new_password)
    
    return jsonify({'success': True})


@app.route('/api/settings/2fa/enable', methods=['POST'])
def enable_2fa():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    import pyotp
    
    # Generate TOTP secret
    totp_secret = pyotp.random_base32()
    
    db.enable_2fa(session['user_id'], totp_secret)
    
    # Generate QR code URI
    user = db.get_user_by_id(session['user_id'])
    totp_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(
        name=user['username'],
        issuer_name='Secure File Vault Pro'
    )
    
    return jsonify({'success': True, 'totp_secret': totp_secret, 'totp_uri': totp_uri})


@app.route('/api/settings/2fa/disable', methods=['POST'])
def disable_2fa():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    db.disable_2fa(session['user_id'])
    
    return jsonify({'success': True})


@app.route('/api/settings/sessions/<session_token>', methods=['DELETE'])
def revoke_session(session_token):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    db.revoke_session(session_token)
    
    return jsonify({'success': True})


@app.route('/api/settings/account/delete', methods=['DELETE'])
def delete_account():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    password = data.get('password')
    
    user = db.get_user_by_id(session['user_id'])
    
    if not check_password_hash(user['password'], password):
        return jsonify({'error': 'Password incorrect'}), 401
    
    # Delete all user files
    files = db.get_user_files(session['user_id'])
    for file in files:
        encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], file['encrypted_name'])
        if os.path.exists(encrypted_path):
            os.remove(encrypted_path)
    
    # Delete user account
    db.delete_user_account(session['user_id'])
    
    session.clear()
    
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
