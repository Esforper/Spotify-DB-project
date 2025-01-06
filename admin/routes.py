from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from services.role_service import RoleService

# Blueprint Initialization
admin_bp = Blueprint('admin', __name__, template_folder='templates')


# 📊 Admin Dashboard
@admin_bp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html', title="Admin Dashboard")


@admin_bp.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    query = request.form.get('query', '')
    user_not_found = False  # Add this flag

    if request.method == 'POST' and query:
        try:
            cur = current_app.config['MYSQL'].connection.cursor()
            sql = """
                SELECT KullaniciID, Isim, Eposta, Rol, UyelikTarihi 
                FROM Kullanici 
                WHERE Isim LIKE %s OR Eposta LIKE %s;
            """
            cur.execute(sql, (f"%{query}%", f"%{query}%"))
            results = cur.fetchall()
            cur.close()

            if not results:
                user_not_found = True  # If no results, set the flag
                flash("User not found.", "warning")  # Flash the warning message

        except Exception as e:
            flash(f"Error: {e}", "danger")
    
    return render_template('admin/search.html', results=results, query=query, user_not_found=user_not_found, title="Search Users/Artists")



# ➕ Admin Add Role
@admin_bp.route('/add-role', methods=['GET', 'POST'])
def add_role():
    role_service = RoleService(current_app.config['MYSQL'])

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password') or 'defaultpassword'
        role = request.form.get('role')

        if not username or not email or not role:
            flash("All fields except password are required!", "danger")
            return redirect(url_for('admin.add_role'))

        try:
            if role_service.user_exists(username):
                role_service.update_user_role(username, email, role)
                flash(f"User '{username}' updated with role '{role}' and email '{email}'.", "success")
            else:
                role_service.add_new_user(username, email, password, role)
                flash(f"New user '{username}' added with role '{role}' and email '{email}'.", "success")

            return redirect(url_for('admin.add_role'))
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")
            return redirect(url_for('admin.add_role'))

    return render_template('admin/add_role.html', title="Add Role")


# 🗑️ Admin Delete Role
@admin_bp.route('/delete-role', methods=['GET', 'POST'])
def delete_role():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        role = request.form.get('role')

        if not username or not email or not role:
            flash("All fields are required!", "danger")
            return redirect(url_for('admin.delete_role'))

        try:
            cur = current_app.config['MYSQL'].connection.cursor()
            sql = """
                DELETE FROM Kullanici 
                WHERE Isim = %s AND Eposta = %s AND Rol = %s;
            """
            cur.execute(sql, (username, email, role))
            current_app.config['MYSQL'].connection.commit()
            cur.close()
            
            flash(f"User '{username}' with role '{role}' has been deleted.", "success")
        except Exception as e:
            flash(f"Error: {e}", "danger")
            return redirect(url_for('admin.delete_role'))
        
        return redirect(url_for('admin.delete_role'))
    
    return render_template('admin/delete_role.html', title="Delete Role")
