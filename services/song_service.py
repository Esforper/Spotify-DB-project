from flask_mysqldb import MySQL
import MySQLdb.cursors

class SongService:
    def __init__(self, mysql: MySQL):
        self.mysql = mysql
        
    def get_songs(self):
        """
        Tüm şarkıları getirir.
        """
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Sarki")
        songs = cur.fetchall()
        cur.close()
        return songs
    
    def get_song_by_id(self, song_id):
        """
        Belirli bir şarkıyı ID'sine göre getirir.
        """
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Sarki WHERE SarkiID = %s", (song_id,))
        song = cur.fetchone()
        cur.close()
        return song
    
    def create_song(self, name, artist, album, duration):
        """
        Yeni bir şarkı oluşturur.
        """
        cur = self.mysql.connection.cursor()
        cur.execute("INSERT INTO Sarki (SarkiAdi, Sanatci, Album, Sure) VALUES (%s, %s, %s, %s)", 
                    (name, artist, album, duration))
        self.mysql.connection.commit()
        cur.close()
        
    def update_song(self, song_id, name=None, artist=None, album=None, duration=None):
        """
        Mevcut bir şarkının bilgilerini günceller.
        """
        cur = self.mysql.connection.cursor()
        
        # Güncelleme için mevcut alanları kontrol et
        if name:
            cur.execute("UPDATE Sarki SET SarkiAdi = %s WHERE SarkiID = %s", (name, song_id))
        if artist:
            cur.execute("UPDATE Sarki SET Sanatci = %s WHERE SarkiID = %s", (artist, song_id))
        if album:
            cur.execute("UPDATE Sarki SET Album = %s WHERE SarkiID = %s", (album, song_id))
        if duration:
            cur.execute("UPDATE Sarki SET Sure = %s WHERE SarkiID = %s", (duration, song_id))
        
        self.mysql.connection.commit()
        cur.close()

    def delete_song(self, song_id):
        """
        Bir şarkıyı siler.
        """
        cur = self.mysql.connection.cursor()
        
        # Şarkıyı silmeden önce, şarkı playlistlerde olup olmadığını kontrol edebiliriz
        cur.execute("DELETE FROM CalmaListesi_Sarkilar WHERE SarkiID = %s", (song_id,))
        cur.execute("DELETE FROM Sarki WHERE SarkiID = %s", (song_id,))
        
        self.mysql.connection.commit()
        cur.close()


    def get_songs_by_playlist(self, playlist_id):
        """
        Belirli bir çalma listesindeki şarkıları getirir.
        """
        cur = self.mysql.connection.cursor()
        cur.execute("""
            SELECT 
                s.SarkiID, s.SarkiAdi, s.Sure, s.YayinTarihi, s.TurID, s.AlbumID, s.SanatciID
            FROM 
                Sarki s
            JOIN 
                CalmaListesi_Sarkilar cls ON s.SarkiID = cls.SarkiID
            WHERE 
                cls.CalmaListesiID = %s
        """, (playlist_id,))
        rows = cur.fetchall()
        cur.close()

        # Veriyi dictionary formatına çevir
        songs = [
            {
                "SarkiID": row[0],
                "SarkiAdi": row[1],
                "Sure": row[2],
                "YayinTarihi": row[3],
                "TurID": row[4],
                "AlbumID": row[5],
                "SanatciID": row[6],
            }
            for row in rows
        ]
        return songs


    
    def get_songs_by_query(self, query):
        cur = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            SELECT SarkiID, SarkiAdi, SanatciID, AlbumID 
            FROM Sarki
            WHERE LOWER(SarkiAdi) LIKE %s
        """, ('%' + query + '%',))  # Sadece şarkı adında arama yapılır
        songs = cur.fetchall()
        cur.close()
        return songs