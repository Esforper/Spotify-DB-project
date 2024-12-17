from flask import Flask, render_template, request, redirect, url_for, session
from admin.routes import admin_bp
from user.routes import user_bp
from artist.routes import artist_bp

# Flask uygulamasını oluştur
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Make sure to set a secret key for sessions

# Blueprint'leri kaydet
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(artist_bp, url_prefix='/artist')

# Temporary users store (for testing purposes)
valid_users = {
    "admin": {"password": "password", "role": "Admin"},
    "user1": {"password": "pass123", "role": "User"},
    "emir": {"password": "mypassword", "role": "Artist"}
}

# Home Route (Library page)
@app.route('/')
def home():
    if 'logged_in' in session:
        role = session.get('role')
        if role == 'Admin':
            return redirect(url_for('admin.dashboard'))
        elif role == 'User':
            return redirect(url_for('user.profile'))
        elif role == 'Artist':
            return redirect(url_for('artist.gallery'))
    return redirect(url_for('login'))

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if username in valid_users and valid_users[username]['password'] == password and valid_users[username]['role'] == role:
            session['logged_in'] = True
            session['username'] = username
            session['role'] = role

            # Kullanıcının rolüne göre yönlendirme
            if role == "Admin":
                return redirect(url_for('admin.dashboard'))
            elif role == "User":
                return redirect(url_for('user.profile'))
            elif role == "Artist":
                return redirect(url_for('artist.gallery'))

        else:
            return render_template('login.html', error="Invalid username, password, or role")
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # Kullanıcı adı zaten var mı?
        if username in valid_users:
            return render_template('signup.html', error="Username already exists")

        # Yeni kullanıcıyı ekle
        valid_users[username] = {"password": password, "role": role}
        session['logged_in'] = True
        session['username'] = username
        session['role'] = role

        # Kullanıcının rolüne göre yönlendirme
        if role == "Admin":
            return redirect(url_for('admin.dashboard'))
        elif role == "User":
            return redirect(url_for('user.profile'))
        elif role == "Artist":
            return redirect(url_for('artist.gallery'))

    return render_template('signup.html')


# Library Route
@app.route('/library')
def library():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('library.html')

# Search Route
@app.route('/search')
def search():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('search.html')

# Profile Route
@app.route('/profile')
def profile():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html')

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Flask uygulamasını çalıştır
if __name__ == '__main__':
    app.run(debug=True)
