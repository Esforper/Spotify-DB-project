from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.user_service import UserService
from services.playlist_service import PlaylistService
from services.song_service import SongService
from services.album_service import AlbumService
from services.artist_service import ArtistService
from flask_mysqldb import MySQL

user_service_instance = UserService()
playlist_service = PlaylistService(mysql=MySQL())
song_service = SongService(mysql=MySQL())
album_service = AlbumService(mysql=MySQL())
artist_service = ArtistService(mysql=MySQL())

user_bp = Blueprint('user', __name__, template_folder='templates')

"""
# Localde playlistleri saklamak için bir liste
Tur = [
    {'TurID': 1, 'TurAdi': 'Pop', 'Aciklama': 'Popüler müzik'},
    {'TurID': 2, 'TurAdi': 'Rock', 'Aciklama': 'Rock müzik'},
]

Album = [
    {'AlbumID': 1, 'AlbumAdi': 'Favoriler', 'YayinTarihi': '2023-01-01', 'TurID': 1, 'SanatciID': 1},
    {'AlbumID': 2, 'AlbumAdi': 'Rock Hits', 'YayinTarihi': '2023-05-10', 'TurID': 2, 'SanatciID': 2},
]

Sarki = [
    {'SarkiID': 1, 'SarkiAdi': 'Şarkı 1', 'Sure': '00:03:45', 'YayinTarihi': '2023-01-10', 'TurID': 1, 'AlbumID': 1, 'SanatciID': 1},
    {'SarkiID': 2, 'SarkiAdi': 'Şarkı 2', 'Sure': '00:04:10', 'YayinTarihi': '2023-01-15', 'TurID': 1, 'AlbumID': 1, 'SanatciID': 1},
    {'SarkiID': 3, 'SarkiAdi': 'Rock Şarkı 1', 'Sure': '00:02:50', 'YayinTarihi': '2023-05-20', 'TurID': 2, 'AlbumID': 2, 'SanatciID': 2},
    {'SarkiID': 4, 'SarkiAdi': 'Rock Şarkı 2', 'Sure': '00:03:15', 'YayinTarihi': '2023-05-25', 'TurID': 2, 'AlbumID': 2, 'SanatciID': 2},
]
CalmaListesi = [
    {'CalmaListesiID': 1, 'CalmaListesiAdi': 'Hareketli Şarkılar', 'KullaniciID': 1},
    {'CalmaListesiID': 2, 'CalmaListesiAdi': 'Yavaş Şarkılar', 'KullaniciID': 1},
]
CalmaListesi_Sarkilar = [
    {'CalmaListesiSarkilarID': 1, 'CalmaListesiID': 1, 'SarkiID': 1},
    {'CalmaListesiSarkilarID': 2, 'CalmaListesiID': 1, 'SarkiID': 3},
    {'CalmaListesiSarkilarID': 3, 'CalmaListesiID': 2, 'SarkiID': 2},
    {'CalmaListesiSarkilarID': 4, 'CalmaListesiID': 2, 'SarkiID': 4},
]
"""


@user_bp.route('/home')
def home():
    playlists = playlist_service.get_playlists(user_id=1)   #user serviceden bilgiler gelecek.
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
        playlist_description = request.form['playlistDescription'] #playlist açıklaması alınıyor.
        # Bu bilgiler anlık olarak işe yaramıyor, daha sonra değiştirilerek silinecek.
        
        # Yeni bir playlist oluşturuyoruz
        playlist_service.create_playlist(name=playlist_name, user_id=1)
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
    playlist_service.delete_song_from_playlist(playlist_id=playlist_index, song_id=song_id)  # Şarkıyı playlist'ten sil    flash('Şarkı playlist\'ten başarıyla silindi!', 'success')
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
    if 'logged_in' not in session or not session['logged_in']:
        flash('Lütfen giriş yapın.', 'danger')
        return redirect(url_for('login'))
    
    # Oturumdaki username'i al
    username = session.get('username')
    print(username)
    
    # user_service üzerinden kullanıcı bilgilerini al
    user = user_service_instance.get_user(username)

    if not user:
        flash('Kullanıcı bilgileri bulunamadı.', 'danger')
        return redirect(url_for('login'))
        
    user_id = 1  # Assuming user_id is hardcoded for now, this could be dynamic in a real app
    # Favori sanatçıları çek
    favorite_artists = artist_service.get_favorite_artists(user_id)

    # Kullanıcı bilgilerini şablona gönder
    return render_template('user/profile.html', username=username, role=user['role'], favorite_artists=favorite_artists)


@user_bp.route('/album/<int:album_id>')
def album_detail(album_id):
    album = album_service.get_album_by_id(album_id)  # Albümü album_service üzerinden al
    if album:
        songs = album_service.get_songs_by_album(album_id)  # Albümdeki şarkıları album_service üzerinden al
        return render_template('user/album_detail.html', album=album, songs=songs)
    flash('Albüm bulunamadı.', 'danger')
    return redirect(url_for('user.search'))




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
    user_id = 1  # Assuming user_id is hardcoded for now, this could be dynamic in a real app
    song_id = request.form.get('song_id')  # Get song ID from form data

    try:
        song_service.add_favorite_song(user_id, song_id)  # Add to favorites
        flash('Şarkı başarıyla favorilere eklendi!', 'success')
    except Exception as e:
        flash(f'Hata: {e}', 'danger')
    
    return redirect(url_for('user.profile'))  # Redirect to profile page or desired page


@user_bp.route('/add_favorite_artist', methods=['POST'])
def add_favorite_artist():
    user_id = 1  # Assuming user_id is hardcoded for now, this could be dynamic in a real app
    artist_id = request.form.get('artist_id')  # Get artist ID from form data

    try:
        artist_service.add_favorite_artist(user_id, artist_id)  # Add artist to favorites
        flash('Sanatçı başarıyla favorilere eklendi!', 'success')
    except Exception as e:
        flash(f'Hata: {e}', 'danger')

    return redirect(url_for('user.profile'))  # Redirect to profile page or desired page

@user_bp.route('/favorite_songs' , methods=['GET'])
def favorite_songs():
    user_id = 1
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
    


