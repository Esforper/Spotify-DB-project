from flask_mysqldb import MySQL
import MySQLdb.cursors

class AlbumService:
    def __init__(self, mysql: MySQL):
        self.mysql = mysql
    
    def get_all_albums(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Album")
        albums = cur.fetchall()
        cur.close()
        return albums

    def get_album_by_id(self, album_id):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Album WHERE AlbumID = %s", (album_id,))
        album = cur.fetchone()
        cur.close()
        return album
    
    def create_album(self, album_name, release_date, genre_id, artist_id):
        cur = self.mysql.connection.cursor()
        cur.execute("""
            INSERT INTO Album (AlbumAdi, YayinTarihi, TurID, SanatciID) 
            VALUES (%s, %s, %s, %s)
        """, (album_name, release_date, genre_id, artist_id))
        self.mysql.connection.commit()
        cur.close()

    def get_songs_by_album(self, album_id):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Sarki WHERE AlbumID = %s", (album_id,))
        songs = cur.fetchall()
        cur.close()
        return songs
    
    def search_albums_by_query(self, query):
        # DictCursor kullanarak verilerinizi sözlük formatında alın
        cur = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            SELECT AlbumID, AlbumAdi, YayinTarihi, TurID, SanatciID
            FROM Album
            WHERE LOWER(AlbumAdi) LIKE %s
        """, ('%' + query + '%',))  # Albüm adı üzerinden arama
        albums = cur.fetchall()
        cur.close()
        return albums

