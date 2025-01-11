from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from services.user_service import UserService
from services.playlist_service import PlaylistService
from services.song_service import SongService
from services.album_service import AlbumService
from services.artist_service import ArtistService
from flask_mysqldb import MySQL

user_service_instance = UserService(mysql=MySQL())
playlist_service = PlaylistService(mysql=MySQL())
song_service = SongService(mysql=MySQL())
album_service = AlbumService(mysql=MySQL())
artist_service = ArtistService(mysql=MySQL())

user_bp = Blueprint('user', __name__, template_folder='templates')

@user_bp.before_request
def load_user():
    if 'email' in session and 'role' in session and 'logged_in' in session:
        user_email = session['email']
        user_role = session.get('role', None)
        user = user_service_instance.get_user(user_email, user_role)
        print("user bilgisi: ",user)
        g.user = user
        print("g.user bilgisi: ",g.user)
        print("g bilgisi", g)
    else:
        g.user = None  # Eğer kullanıcı yoksa None atayın.

@user_bp.route('/home')
def home():

    playlists = playlist_service.get_playlists(user_id=g.user['KullaniciID'])   #user serviceden bilgiler gelecek.
    print("session bilgisi: ",session)
    return render_template('user/home.html', title="User library" ,playlists=playlists)


@user_bp.route('/playlist/<int:playlist_index>')
def playlist_detail(playlist_index):
    """
    Çalma listesi detaylarını görüntüler.
    """
    try:
        # Çalma listesini alın
        playlist = playlist_service.get_playlist_by_id(playlist_index)

        if not playlist:
            flash('Hata: Çalma listesi bulunamadı.', 'danger')
            return redirect(url_for('user.home'))

        # Çalma listesindeki şarkıları alın
        playlist_songs = song_service.get_songs_by_playlist(playlist_index)
        print("playlist kontrolu: ",playlist_songs)
        
        return render_template(
            'user/playlist_detail.html',
            playlist=playlist,
            songs=playlist_songs,
            playlist_index=playlist_index
        )
    except Exception as e:
        flash(f'Hata: {e}', 'danger')
        return redirect(url_for('user.home'))




@user_bp.route('/create_playlist', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'POST':
        playlist_name = request.form['playlistName']
        playlist_description = request.form['playlistDescription']
        
        playlist_service.create_playlist(name=playlist_name, user_id=g.user['KullaniciID'])
        flash('Playlist başarıyla oluşturuldu!', 'success')
        return redirect(url_for('user.home'))
    return render_template('user/create_playlist.html')



@user_bp.route('/delete_playlist/<int:playlist_index>', methods=['POST'])
def delete_playlist(playlist_index):
    try:
        # Seçilen playlist'i listeden çıkarıyoruz
        playlist_service.delete_playlist(playlist_id=playlist_index)
        # Playlist silindiğinde, bu playlist'e ait tüm şarkıları da silelim
        flash('Playlist başarıyla silindi!', 'success')
    except IndexError:
        flash('Hata: Playlist bulunamadı.', 'danger')
    return redirect(url_for('user.home'))


@user_bp.route('/delete_song_from_playlist/<int:playlist_index>/<int:song_id>', methods=['POST'])
def delete_song_from_playlist(playlist_index, song_id):
    # Playlist'ten belirtilen şarkıyı çıkaralım
    playlist_service.delete_song_from_playlist(playlist_id=playlist_index, song_id=song_id)
    return redirect(url_for('user.playlist_detail', playlist_index=playlist_index))

@user_bp.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('q', '').lower()
    results = {'songs': [], 'albums': [], 'artists': []}

    if query:
        # Şarkıları sorgula
        results['songs'] = song_service.get_songs_by_query(query)
        
        # Albümleri sorgula
        results['albums'] = album_service.search_albums_by_query(query)
        
        # Playlistleri sorgula
        results['artists'] = artist_service.search_artist_by_query(query)
        print(results['artists'])
    return render_template('user/search.html', results=results, query=query)



@user_bp.route('/profile')
def profile():
    # Kullanıcının giriş yapıp yapmadığını kontrol et
    if not g.user:
        flash('Lütfen giriş yapın.', 'danger')
        return redirect(url_for('login'))
    
    # Kullanıcı bilgilerini g.user üzerinden al
    email = g.user['Eposta']  # Veya 'username' alanını kullanıyorsanız buna göre düzenleyin
    user_id = g.user['KullaniciID']
    role=g.user['Rol']
    # user_service üzerinden kullanıcı bilgilerini al
    user = user_service_instance.get_user(email, role)
        
    user_id=g.user['KullaniciID']
    # Favori sanatçıları çek
    favorite_artists = artist_service.get_favorite_artists(user_id)

    # Kullanıcı bilgilerini şablona gönder
    return render_template(
    'user/profile.html',
    username=user.get('Isim'),
    email=g.user['Eposta'],
    role=g.user['Rol'],
    favorite_artists=favorite_artists
)



@user_bp.route('/album/<int:album_id>', methods=['GET', 'POST'])
def album_detail(album_id):
    album = album_service.get_album_by_id(album_id)  # Albümü album_service üzerinden al
    print("album kontrolü: ",album)
    if not album:
        flash('Albüm bulunamadı.', 'danger')
        return redirect(url_for('user.search'))

    # Albüme ait şarkılar
    songs = album_service.get_songs_by_album(album_id)

    comments = album_service.get_comments_by_album(album_id)

    if request.method == 'POST':
        content = request.form['comment']
        
        user_id=g.user['KullaniciID'] 
        if content.strip():
            album_service.add_comment_to_album(album_id, user_id, content)
            flash('Comment added successfully!', 'success')
            return redirect(url_for('user.album_detail', album_id=album_id))

    return render_template('user/album_detail.html', album=album, songs=songs, comments=comments)



@user_bp.route('/search_song_to_add', methods=['GET'])
def search_song_to_add():
    query = request.args.get('q', '').lower()
    playlist_id = request.args.get('playlist_id', type=int)
    songs = []

    if query:
        # Şarkı arama işlemi
        songs = song_service.get_songs_by_query(query)

    return render_template('user/search_song_to_add.html', songs=songs, query=query, playlist_id=playlist_id)

@user_bp.route('/add_song_to_playlist/<int:playlist_id>/<int:song_id>', methods=['POST'])
def add_song_to_playlist(playlist_id, song_id):
    try:
        # Şarkıyı çalma listesine ekleme işlemi
        playlist_service.add_song_to_playlist(playlist_id=playlist_id, song_id=song_id)
        flash('Şarkı başarıyla çalma listesine eklendi!', 'success')
    except Exception as e:
        flash(f'Hata: {e}', 'danger')
    return redirect(url_for('user.playlist_detail', playlist_index=playlist_id))




@user_bp.route('/add_favorite_song', methods=['POST'])
def add_favorite_song():
    user_id=g.user['KullaniciID']
    song_id = request.form.get('song_id')  # Get song ID from form data

    try:
        song_service.add_favorite_song(user_id, song_id)  # Add to favorites
        flash('Şarkı başarıyla favorilere eklendi!', 'success')
    except Exception as e:
        flash(f'Hata: {e}', 'danger')
    
    return redirect(url_for('user.home')) 


@user_bp.route('/add_favorite_artist', methods=['POST'])
def add_favorite_artist():
    user_id=g.user['KullaniciID']
    artist_id = request.form.get('artist_id') 

    try:
        artist_service.add_favorite_artist(user_id, artist_id)  
        flash('Sanatçı başarıyla favorilere eklendi!', 'success')
    except Exception as e:
        flash(f'Hata: {e}', 'danger')

    return redirect(url_for('user.profile')) 

@user_bp.route('/favorite_songs' , methods=['GET'])
def favorite_songs():
    user_id=g.user['KullaniciID']
    try:
        favorite_songs = song_service.get_favorite_songs(user_id)
        print("Log : favorite song - ",favorite_songs)
        return render_template(
            'user/favorite_songs.html',
            songs=favorite_songs
        )
    except Exception as e:
        flash(f'Hata: {e}', 'danger')
        return redirect(url_for('user.profile'))
    


