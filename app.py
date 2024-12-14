from flask import Flask, render_template, request, redirect, session, url_for, jsonify

# Flask uygulamasını oluştur
app = Flask(__name__)
app.secret_key = "your_secret_key"  # For session management

# Root route
@app.route('/')
def index():
    # Redirect to login if not logged in
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return redirect(url_for('library'))  # If logged in, go to the library

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Example credentials for testing
    valid_users = {
        "admin": "password",
        "user1": "pass123",
        "emir": "mypassword"
    }

    if request.method == 'POST':
        # Retrieve form data
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # Validate username and password
        if username in valid_users and valid_users[username] == password:
            session['logged_in'] = True
            session['username'] = username
            session['role'] = role
            return redirect(url_for('library'))
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')


# Logout page
@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('login'))

# Protected routes
@app.route('/library')
def library():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('library.html')

@app.route('/search')
def search():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('search.html')

@app.route('/profile')
def profile():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('profile.html')

# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

# Flask uygulamasını çalıştır
if __name__ == '__main__':
    app.run(debug=True)
