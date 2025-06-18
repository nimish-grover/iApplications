from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
import os
import datetime
from flask_login import login_required, current_user
from functools import wraps
import codecs

ERROR_LOG_DIR = 'logs'

# Developer access decorator
def developer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

blp = Blueprint('developer', __name__, url_prefix='/dev')

# Custom Jinja2 filter for timestamp formatting
@blp.app_template_filter('strftime')
def _jinja2_filter_datetime(format, timestamp):
    date = datetime.datetime.fromtimestamp(timestamp)
    return date.strftime(format)

@blp.route('/errors', methods=['GET', 'POST'])
@login_required
@developer_required
def error_logs():
    # Create logs directory if it doesn't exist
    if not os.path.exists(ERROR_LOG_DIR):
        os.makedirs(ERROR_LOG_DIR)

    # Get log files and sort by modification time (newest first)
    log_files = [f for f in os.listdir(ERROR_LOG_DIR) if os.path.isfile(os.path.join(ERROR_LOG_DIR, f))]
    log_files.sort(key=lambda x: os.path.getmtime(os.path.join(ERROR_LOG_DIR, x)), reverse=True)
    
    selected_file = request.args.get('file')
    file_content = ""

    if selected_file and selected_file in log_files:
        try:
            file_path = os.path.join(ERROR_LOG_DIR, selected_file)
            
            # First try to read as text with different encodings
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        file_content = f.read()
                    print(f"Successfully read file with encoding: {encoding}")
                    break
                except UnicodeDecodeError:
                    continue
            
            # If all text encodings fail, read as binary and decode with replacement
            if not file_content:
                print("Reading file in binary mode")
                with open(file_path, 'rb') as f:
                    binary_content = f.read()
                    file_content = binary_content.decode('utf-8', errors='replace')
            
            # Add a debug message at the end of the content to verify it's being read
            file_content += "\n\n--- Debug Info: File successfully read ---"
            
            # Print content length for debugging
            print(f"File content length: {len(file_content)}")
            
            # If the content is still empty, add a message
            if not file_content.strip():
                file_content = "File is empty or could not be read properly."
        
        except Exception as e:
            error_msg = f"Error reading file: {str(e)}"
            print(error_msg)
            flash(error_msg, "danger")
            file_content = error_msg
    else:
        if selected_file:
            flash(f"File not found: {selected_file}", "warning")

    return render_template('developer/view_error.html', 
                          files=log_files, 
                          content=file_content, 
                          selected_file=selected_file,
                          ERROR_LOG_DIR=ERROR_LOG_DIR,
                          os=os)


@blp.route('/error_delete', methods=['POST'])
@login_required
@developer_required
def delete_log_file():
    filename = request.form.get('filename')
    if filename == "all":
        try:
            deleted_count = 0
            for f in os.listdir(ERROR_LOG_DIR):
                file_path = os.path.join(ERROR_LOG_DIR, f)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted_count += 1
            flash(f"All log files deleted ({deleted_count} files).", "success")
        except Exception as e:
            flash(f"Error deleting files: {str(e)}", "danger")
    else:
        file_path = os.path.join(ERROR_LOG_DIR, filename)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                flash(f"File '{filename}' deleted successfully.", "success")
            else:
                flash(f"File '{filename}' not found.", "warning")
        except Exception as e:
            flash(f"Error deleting file: {str(e)}", "danger")
    
    return redirect(url_for('developer.error_logs'))