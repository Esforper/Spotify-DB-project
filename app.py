from flask import Flask, render_template, request, redirect, url_for, session

# Flask uygulamasını oluştur
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Make sure to set a secret key for sessions

# Temporary users store (for testing purposes)
valid_users = {
    "admin": {"password": "password", "role": "Admin"},
    "user1": {"password": "pass123", "role": "User"},
    "emir": {"password": "mypassword", "role": "User"}
}

# Home Route (Library page)
@app.route('/')
def home():
    if 'logged_in' in session:
        return redirect(url_for('library'))
    return redirect(url_for('login'))

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if username in valid_users and valid_users[username]['password'] == password:
            session['logged_in'] = True
            session['username'] = username
            session['role'] = role
            return redirect(url_for('library'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # Check if username already exists
        if username in valid_users:
            return render_template('signup.html', error="Username already exists")

        # Add the new user to the valid_users dictionary
        valid_users[username] = {"password": password, "role": role}
        session['logged_in'] = True
        session['username'] = username
        session['role'] = role
        return redirect(url_for('library'))

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
