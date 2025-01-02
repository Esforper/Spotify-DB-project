from flask import Flask, render_template, request, redirect, url_for, session, flash
from admin.routes import admin_bp
from artist.routes import artist_bp
from user.routes import user_bp
from services import user_service
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Secret key for sessions

user_service = user_service.UserService()

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'  # Change if using a different host
app.config['MYSQL_USER'] = 'root'       # Your MySQL username
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')       # Get password from .env
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')  

mysql = MySQL(app)
app.config['MYSQL'] = mysql

# Register Blueprints
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(artist_bp, url_prefix='/artist')
app.register_blueprint(user_bp, url_prefix='/user')

@app.route('/test-db')
def test_db():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Album;")
    data = cur.fetchall()  # Fetch all rows
    cur.close()
    return {"users": data}

# Home Route (redirects based on role)
@app.route('/')
def home():
    if 'logged_in' in session:
        role = session.get('role')
        if role == 'Admin':
            return redirect(url_for('admin.dashboard'))
        elif role == 'User':
            return redirect(url_for('user.home'))
        elif role == 'Artist':
            return redirect(url_for('artist.profile'))
    return redirect(url_for('login'))

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        role = request.form['role'].strip()

        user = user_service.validate_user(username, password, role) #user service bağlantısı.
        if user:
                session['logged_in'] = True
                session['username'] = username
                session['role'] = role
                # Redirect based on role
                if role == "Admin":
                    return redirect(url_for('admin.dashboard'))
                elif role == "User":
                    return redirect(url_for('user.home'))
                elif role == "Artist":
                    return redirect(url_for('artist.profile'))
        return render_template('login.html', error="Invalid credentials or role")
    return render_template('login.html')

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        role = request.form['role'].strip()

        # Check if user already exists in user_service
        if user_service.get_user(username):
            return render_template('signup.html', error="Username already exists")

        # Normally, you would add user to the database here, but for now, just mock it
        user_service.users[username] = {"password": password, "role": role}
        session['logged_in'] = True
        session['username'] = username
        session['role'] = role

        # Redirect based on role
        if role == "Admin":
            return redirect(url_for('admin.dashboard'))
        elif role == "User":
            return redirect(url_for('user.home'))
        elif role == "Artist":
            return redirect(url_for('artist.profile'))

    return render_template('signup.html')


@app.route('/logout')
def logout():
    username = session.get('username')
    if username:
        user_service.logout_user(username)
    session.clear()
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('login'))


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
