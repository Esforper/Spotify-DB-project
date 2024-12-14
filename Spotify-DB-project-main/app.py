from flask import Flask, render_template, request, jsonify

# Flask uygulamasını oluştur
app = Flask(__name__)

# Ana sayfa route'u (Library'ye yönlendir)
@app.route('/')
def home():
    return library()

# Search sayfası
@app.route('/search')
def search():
    return render_template('search.html')

# Library sayfası
@app.route('/library')
def library():
    return render_template('library.html')

# Profile sayfası
@app.route('/profile')
def profile():
    return render_template('profile.html')

# Özel hata sayfaları
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

# Flask uygulamasını çalıştır
if __name__ == '__main__':
    app.run(debug=True)