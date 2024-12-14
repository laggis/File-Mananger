from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify
import os
from functools import wraps
from users import UserManager
from config import ConfigManager
import mimetypes
from werkzeug.utils import secure_filename
import json
import shutil
import humanize
from datetime import datetime
import tempfile
import zipfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Initialize user manager
user_manager = UserManager()
user_manager.init_users()  # Initialize default admin user

# Set root directory to C:\inetpub
ROOT_DIR = r'C:\inetpub'

# Create the root directory if it doesn't exist
if not os.path.exists(ROOT_DIR):
    try:
        os.makedirs(ROOT_DIR)
        app.logger.info(f"Created root directory at {ROOT_DIR}")
    except Exception as e:
        app.logger.error(f"Failed to create root directory: {str(e)}")
        ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
        app.logger.warning(f"Falling back to application directory: {ROOT_DIR}")

app.config['UPLOAD_FOLDER'] = ROOT_DIR
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'zip', 'rar'}
config_manager = ConfigManager()

# Configuration for download limits
DOWNLOAD_LIMITS = {
    'default': 50,  # Default daily download limit for regular users
    'admin': 1000   # Daily download limit for admin users
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or not user_manager.is_admin(session['username']):
            flash('Admin privileges required.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        success, message = user_manager.verify_user(username, password)
        if success:
            session['username'] = message  # message contains actual username with correct case
            session['is_admin'] = user_manager.is_admin(message)
            return redirect(url_for('index'))
        else:
            flash(message, 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        success, message = user_manager.add_user(username, password)
        if success:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'error')
    
    return render_template('register.html')

@app.route('/admin')
@login_required
@admin_required
def admin():
    return render_template('admin.html',
                         users=user_manager.get_users(),
                         is_admin=session.get('is_admin', False))

@app.route('/admin/create_user', methods=['POST'])
@login_required
@admin_required
def admin_create_user():
    username = request.form.get('username')
    password = request.form.get('password')
    is_admin = request.form.get('is_admin') == 'true'
    
    if not username or not password:
        flash('Username and password are required.', 'error')
        return redirect(url_for('admin'))
    
    if user_manager.create_user(username, password, is_admin):
        flash('User created successfully.', 'success')
    else:
        flash('Failed to create user. Username might already exist.', 'error')
    
    return redirect(url_for('admin'))

@app.route('/admin/remove_user', methods=['POST'])
@login_required
@admin_required
def admin_remove_user():
    username = request.form.get('username')
    if not username:
        flash('Username is required.', 'error')
        return redirect(url_for('admin'))
    
    if username == session.get('username'):
        flash('Cannot remove your own account.', 'error')
        return redirect(url_for('admin'))
    
    if user_manager.remove_user(username):
        flash('User removed successfully.', 'success')
    else:
        flash('Failed to remove user.', 'error')
    
    return redirect(url_for('admin'))

@app.route('/admin/block_item', methods=['POST'])
@login_required
@admin_required
def admin_block_item():
    path = request.form.get('path')
    if not path:
        return jsonify({'error': 'No path specified'}), 400
    
    if config_manager.block_item(path):
        return jsonify({'message': 'Item blocked successfully'})
    else:
        return jsonify({'error': 'Failed to block item'}), 500

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([current_password, new_password, confirm_password]):
            flash('All fields are required')
            return redirect(url_for('profile'))
        
        if new_password != confirm_password:
            flash('New passwords do not match')
            return redirect(url_for('profile'))
        
        success, message = user_manager.change_password(session['username'], current_password, new_password)
        flash(message)
        if success:
            return redirect(url_for('login'))
        return redirect(url_for('profile'))
    
    return render_template('profile.html', 
                         username=session['username'],
                         is_admin=session.get('is_admin', False))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_info(path):
    stats = os.stat(path)
    mime_type, _ = mimetypes.guess_type(path)
    return {
        'name': os.path.basename(path),
        'path': path,
        'size': humanize.naturalsize(stats.st_size),
        'modified': datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
        'type': mime_type or 'application/octet-stream',
        'is_directory': os.path.isdir(path)
    }

def get_directory_contents(path):
    try:
        # Ensure the path is within ROOT_DIR
        abs_path = os.path.abspath(path)
        if not abs_path.startswith(ROOT_DIR):
            abs_path = ROOT_DIR
        
        # Security check
        if not os.path.commonprefix([abs_path, ROOT_DIR]) == ROOT_DIR:
            return []

        items = []
        for item in os.listdir(abs_path):
            item_path = os.path.join(abs_path, item)
            is_dir = os.path.isdir(item_path)
            
            # Skip if item is blocked (unless user is admin)
            if config_manager.is_blocked(item_path, session.get('is_admin', False)):
                continue
            
            # Get relative path from ROOT_DIR
            rel_path = os.path.relpath(item_path, ROOT_DIR).replace('\\', '/')
            
            try:
                size = os.path.getsize(item_path) if not is_dir else None
            except OSError:
                size = 0  # Set size to 0 if unable to get size
                
            items.append({
                'name': item,
                'is_directory': is_dir,
                'path': rel_path,
                'size': size
            })
            
        return sorted(items, key=lambda x: (not x['is_directory'], x['name'].lower()))
    except Exception as e:
        app.logger.error(f"Error getting directory contents: {str(e)}")
        return []

@app.route('/')
@app.route('/<path:subpath>')
@login_required
def index(subpath=''):
    base_path = os.path.abspath(os.path.join(ROOT_DIR, subpath))
    
    if not os.path.exists(base_path):
        return "Path not found", 404
    
    if os.path.isfile(base_path):
        if config_manager.is_blocked(base_path, session.get('is_admin', False)):
            return "Access denied", 403
        return send_file(base_path)
    
    files = get_directory_contents(base_path)
    parent = os.path.dirname(base_path) if subpath else None
    return render_template('index.html', 
                         files=files, 
                         current_path=subpath, 
                         parent=parent,
                         is_admin=session.get('is_admin', False))

@app.route('/delete', methods=['POST'])
@login_required
@admin_required
def delete():
    try:
        file_path = request.form.get('path')
        if not file_path:
            flash('No file path provided.', 'error')
            return redirect(url_for('index'))

        abs_path = os.path.join(ROOT_DIR, file_path.lstrip('/'))
        
        if not is_safe_path(abs_path):
            flash('Invalid file path.', 'error')
            return redirect(url_for('index'))

        if os.path.exists(abs_path):
            if os.path.isfile(abs_path):
                os.remove(abs_path)
            elif os.path.isdir(abs_path):
                shutil.rmtree(abs_path)
            flash('Item deleted successfully.', 'success')
        else:
            flash('File not found.', 'error')
            
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error deleting item: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
@login_required
@admin_required
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File uploaded successfully', 'success')
    else:
        flash('File type not allowed', 'error')
    
    return redirect(url_for('index'))

@app.route('/create-folder', methods=['POST'])
@login_required
@admin_required
def create_folder():
    folder_name = request.form.get('folder_name')
    if not folder_name:
        flash('Please provide a folder name.', 'error')
        return redirect(url_for('index'))

    # Clean the folder name
    folder_name = secure_filename(folder_name)
    new_folder_path = os.path.join(ROOT_DIR, folder_name)

    try:
        os.makedirs(new_folder_path)
        flash('Folder created successfully.', 'success')
    except FileExistsError:
        flash('A folder with this name already exists.', 'error')
    except Exception as e:
        flash(f'Error creating folder: {str(e)}', 'error')

    return redirect(url_for('index'))

@app.route('/download/<path:filename>')
@login_required
def download_file(filename):
    try:
        # Get the absolute path of the file
        file_path = os.path.join(ROOT_DIR, filename)
        
        # Security check: Ensure the file is within the allowed directory
        if not os.path.commonprefix([os.path.abspath(file_path), ROOT_DIR]) == ROOT_DIR:
            return jsonify({'error': 'Access denied'}), 403
        
        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        # Check if file is in blocked list
        if config_manager.is_blocked(file_path, session.get('is_admin', False)):
            return jsonify({'error': 'File is blocked'}), 403
        
        # Get user's current download count
        current_count = get_user_download_count(session['username'])
        daily_limit = DOWNLOAD_LIMITS['admin'] if user_manager.is_admin(session['username']) else DOWNLOAD_LIMITS['default']
        
        # Check if user has exceeded their daily limit
        if current_count >= daily_limit:
            return jsonify({'error': 'Daily download limit reached'}), 429
        
        # Update download count before processing download
        update_user_download_count(session['username'])
        
        # Send the file
        return send_file(file_path, as_attachment=True)
        
    except Exception as e:
        app.logger.error(f"Download error: {str(e)}")
        return jsonify({'error': 'Download failed'}), 500

@app.route('/download-multiple', methods=['POST'])
@login_required
def download_multiple():
    try:
        data = request.get_json()
        if not data or 'files' not in data:
            return jsonify({'error': 'No files specified'}), 400
        
        files = data['files']
        if not files:
            return jsonify({'error': 'Empty file list'}), 400
        
        # Create a temporary directory in the current working directory
        temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            # Create a unique filename for the zip
            zip_filename = f'selected_files_{int(datetime.now().timestamp())}.zip'
            zip_path = os.path.join(temp_dir, zip_filename)
            
            # Create zip file
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in files:
                    # Clean the file path and make it absolute
                    clean_path = file_path.replace('\\', '/').lstrip('/')
                    abs_path = os.path.abspath(os.path.join(ROOT_DIR, clean_path))
                    
                    # Security checks
                    if not abs_path.startswith(ROOT_DIR):
                        continue
                    
                    if not os.path.exists(abs_path) or not os.path.isfile(abs_path):
                        continue
                    
                    # Check if file is blocked
                    if config_manager.is_blocked(abs_path, session.get('is_admin', False)):
                        continue
                    
                    try:
                        # Add file to zip with relative path as name
                        arcname = os.path.basename(file_path)
                        zipf.write(abs_path, arcname)
                    except Exception as e:
                        continue
            
            try:
                # Send the file and then delete it
                response = send_file(
                    zip_path,
                    mimetype='application/zip',
                    as_attachment=True,
                    download_name='selected_files.zip'
                )
                
                # Delete the zip file after sending
                @response.call_on_close
                def cleanup():
                    try:
                        os.remove(zip_path)
                    except:
                        pass
                
                return response
                
            except Exception as e:
                # Clean up if sending fails
                try:
                    os.remove(zip_path)
                except:
                    pass
                return jsonify({'error': 'Failed to send zip file'}), 500
                
        except Exception as e:
            return jsonify({'error': 'Failed to create zip file'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_user_download_count(username):
    # Implement logic to get user's current download count
    pass

def update_user_download_count(username):
    # Implement logic to update user's download count
    pass

def is_safe_path(path):
    return os.path.commonprefix([path, ROOT_DIR]) == ROOT_DIR

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)