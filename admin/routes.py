from flask import Blueprint, render_template, request, redirect, url_for, flash

admin_bp = Blueprint('admin', __name__, template_folder='templates')

# Admin Dashboard
@admin_bp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html', title="Admin Dashboard")

# Admin Search Page
@admin_bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        # Mock search result
        result = f"Results for '{query}'"
        return render_template('admin/search.html', result=result, title="Search Users")
    return render_template('admin/search.html', title="Search Users")

# Admin Add Role Page
@admin_bp.route('/add-role', methods=['GET', 'POST'])
def add_role():
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        # Mock adding role logic
        flash(f"Role '{role}' added to user '{username}'.", "success")
        return redirect(url_for('admin.add_role'))
    return render_template('admin/add_role.html', title="Add Role")

# Admin Delete Role Page
@admin_bp.route('/delete-role', methods=['GET', 'POST'])
def delete_role():
    if request.method == 'POST':
        username = request.form['username']
        # Mock delete role logic
        flash(f"Role for user '{username}' has been deleted.", "danger")
        return redirect(url_for('admin.delete_role'))
    return render_template('admin/delete_role.html', title="Delete Role")
