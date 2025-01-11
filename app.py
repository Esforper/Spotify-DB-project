from flask import Flask, render_template, request, redirect, url_for, session, flash
from admin.routes import admin_bp
from artist.routes import artist_bp
from user.routes import user_bp
from services.user_service import UserService  # Yeni UserService import #yeni
# MySQL bağlantısını zaten app.py içinde tanımlamıştık
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Secret key for sessions



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

user_service = UserService(mysql=mysql)  # MySQL bağlantısını UserService'e geçiyoruz. yeni

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
    # Oturum bilgisi kontrolü
    if 'logged_in' in session and session['logged_in']:
        email = session.get('email')
        role = session.get('role')

        # Kullanıcı bilgilerini doğrulamak için user_service kullan
        user = user_service.get_user(email, role)  # user_service'den kullanıcıyı al
        if user:
            # Role göre yönlendirme yap
            if role == 'Yonetici':
                return redirect(url_for('admin.dashboard'))
            elif role == 'Dinleyici':
                return redirect(url_for('user.home'))
            elif role == 'Sanatci':
                return redirect(url_for('artist.profile'))

    # Eğer kullanıcı yoksa veya oturum geçersizse, oturumu temizle ve login sayfasına yönlendir
    session.clear()
    return redirect(url_for('login'))

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()    #normalde username olarak loginden alınıyor ama email olarak değiştirildi.
        password = request.form['password'].strip()
        role = request.form['role'].strip()
            
        print("User bilgileri", email, password, role)
        user = user_service.validate_user(email, password, role) #user service bağlantısı.
        print("User bilgileri", user)
        if user:
                session['logged_in'] = True
                session['email'] = email
                session['role'] = role
                # Redirect based on role
                if role == "Yönetici":
                    return redirect(url_for('admin.dashboard'))
                elif role == "Dinleyici":
                    return redirect(url_for('user.home'))
                elif role == "Sanatçı":
                    return redirect(url_for('artist.profile'))
        return render_template('login.html', error="Invalid credentials or role")
    return render_template('login.html')

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['username'].strip()
        email = request.form['email'].strip() 
        password = request.form['password'].strip()
        role = request.form['role'].strip()

        # Kullanıcının zaten mevcut olup olmadığını kontrol et
        if user_service.get_user(email, role):
            return render_template('signup.html', error="Email already exists")

        # Kullanıcıyı kaydet
        success = False
        if role == "Yönetici":
            success = user_service.create_admin(name, email, password)
        else:
            success = user_service.create_user(name, email, password, role)


        if success:
            # Başarılı kayıt sonrası oturum aç
            session['logged_in'] = True
            session['username'] = name
            session['email'] = email
            session['role'] = role

            # Rol bazlı yönlendirme
            if role == "Yönetici":
                return redirect(url_for('admin.dashboard'))
            elif role == "Dinleyici":
                return redirect(url_for('user.home'))
            elif role == "Sanatçı":
                return redirect(url_for('artist.profile'))
        return render_template('signup.html', error="An error occurred during signup")

    return render_template('signup.html')


@app.route('/logout')
def logout():
    username = session.get('username')
    if username:
        user_service.logout_user(username)
    session.clear()
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
