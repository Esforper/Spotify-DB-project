from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.user_service import UserService
user_service_instance = UserService()

user_bp = Blueprint('user', __name__, template_folder='templates')

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



@user_bp.route('/home')
def home():
    return render_template('user/home.html', title="User library" ,playlists=CalmaListesi)

@user_bp.route('/playlist/<int:playlist_index>')
def playlist_detail(playlist_index):
    try:
        playlist = CalmaListesi[playlist_index - 1]  # Adjust for zero-based index
        song_ids = [item['SarkiID'] for item in CalmaListesi_Sarkilar if item['CalmaListesiID'] == playlist['CalmaListesiID']]
        playlist_songs = [song for song in Sarki if song['SarkiID'] in song_ids]
        return render_template('user/playlist_detail.html', playlist=playlist, songs=playlist_songs, playlist_index=playlist_index)
    except IndexError:
        flash('Hata: Playlist bulunamadı.', 'danger')
        return redirect(url_for('user.home'))



@user_bp.route('/create_playlist', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'POST':
        playlist_name = request.form['playlistName']
        playlist_description = request.form['playlistDescription']
        # Yeni bir playlist oluşturuyoruz
        new_playlist = {
            'CalmaListesiID': len(CalmaListesi) + 1,
            'CalmaListesiAdi': playlist_name,
            'KullaniciID': 1  # Örnek olarak, kullanıcı ID
        }
        CalmaListesi.append(new_playlist)
        flash('Playlist başarıyla oluşturuldu!', 'success')
        return redirect(url_for('user.home'))
    return render_template('user/create_playlist.html')



@user_bp.route('/delete_playlist/<int:playlist_index>', methods=['POST'])
def delete_playlist(playlist_index):
    try:
        # Seçilen playlist'i listeden çıkarıyoruz
        deleted_playlist = CalmaListesi.pop(playlist_index)
        # Playlist silindiğinde, bu playlist'e ait tüm şarkıları da silelim
        global CalmaListesi_Sarkilar
        CalmaListesi_Sarkilar = [item for item in CalmaListesi_Sarkilar if item['CalmaListesiID'] != deleted_playlist['CalmaListesiID']]
        flash('Playlist başarıyla silindi!', 'success')
    except IndexError:
        flash('Hata: Playlist bulunamadı.', 'danger')
    return redirect(url_for('user.home'))

@user_bp.route('/delete_song_from_playlist/<int:playlist_index>/<int:song_id>', methods=['POST'])
def delete_song_from_playlist(playlist_index, song_id):
    # Playlist'ten belirtilen şarkıyı çıkaralım
    global CalmaListesi_Sarkilar
    CalmaListesi_Sarkilar = [item for item in CalmaListesi_Sarkilar if not (item['CalmaListesiID'] == CalmaListesi[playlist_index]['CalmaListesiID'] and item['SarkiID'] == song_id)]
    flash('Şarkı playlist\'ten başarıyla silindi!', 'success')
    return redirect(url_for('user.playlist_detail', playlist_index=playlist_index))

@user_bp.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('q', '').lower()
    results = {'songs': [], 'albums': [], 'artists': []}

    if query:  # Kullanıcı arama yaptığında sonuçları filtrele
        results['songs'] = [song for song in Sarki if query in song['SarkiAdi'].lower()]
        results['albums'] = [album for album in Album if query in album['AlbumAdi'].lower()]
        # Sanatçı ID'yi örnekle anladığım kadarıyla string araması gerekiyordu:
        results['artists'] = list(set(song['SanatciID'] for song in Sarki if query in str(song['SanatciID'])))

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

    # Kullanıcı bilgilerini şablona gönder
    return render_template('user/profile.html', username=username, role=user['role'])


@user_bp.route('/album/<int:album_id>')
def album_detail(album_id):
    album = next((album for album in Album if album['AlbumID'] == album_id), None)
    if album:
        songs = [song for song in Sarki if song['AlbumID'] == album_id]
        return render_template('user/album_detail.html', album=album, songs=songs)
    flash('Albüm bulunamadı.', 'danger')
    return redirect(url_for('user.search'))
