from flask import Blueprint, render_template, request, redirect, url_for, flash

user_bp = Blueprint('user', __name__, template_folder='templates')

# Localde playlistleri saklamak için bir liste
playlists = []


@user_bp.route('/home')
def home():
    return render_template('user/home.html', title="User library" ,playlists=playlists)

@user_bp.route('/create_playlist', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'POST':
        playlist_name = request.form['playlistName']
        playlist_description = request.form['playlistDescription']
        playlists.append({
            'name': playlist_name,
            'description': playlist_description
        })
        flash('Playlist başarıyla oluşturuldu!', 'success')
        return redirect(url_for('user.home'))
    return render_template('user/create_playlist.html')

@user_bp.route('/delete_playlist/<int:playlist_index>', methods=['POST'])
def delete_playlist(playlist_index):
    try:
        playlists.pop(playlist_index)
        flash('Playlist başarıyla silindi!', 'success')
    except IndexError:
        flash('Hata: Playlist bulunamadı.', 'danger')
    return redirect(url_for('user.home'))



@user_bp.route('/search')
def search():
    return render_template('user/search.html', title="User search")

@user_bp.route('/profile')
def profile():
    return render_template('user/profile.html', title="User profile")
