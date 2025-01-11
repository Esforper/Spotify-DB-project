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
        cur = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            SELECT 
                s.SarkiID, 
                s.SarkiAdi,
                s.Sure, 
                s.YayinTarihi AS SarkiYayinTarihi, 
                a.AlbumAdi, 
                a.YayinTarihi AS AlbumYayinTarihi,
                sanat.SanatciIsmi 
            FROM 
                Sarki s
            JOIN 
                CalmaListesi_Sarkilar cls ON s.SarkiID = cls.SarkiID
            LEFT JOIN 
                Album a ON s.AlbumID = a.AlbumID
            LEFT JOIN 
                Sanatci sanat ON s.SanatciID = sanat.SanatciID
            WHERE 
                cls.CalmaListesiID = %s
        """, (playlist_id,))
        songs = cur.fetchall()
        print("song service içindeki kontrol", songs)
        cur.close()
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
    
    def add_favorite_song(self,user_id, song_id):
        cur = self.mysql.connection.cursor()
        cur.execute(
            "INSERT INTO FavoriSarkilar (KullaniciID, SarkiID) VALUES (%s, %s)",
            (user_id, song_id)
        )
        self.mysql.connection.commit()
        cur.close()
    
    def get_favorite_songs(self, user_id):
        cur = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = """
            SELECT 
                S.SarkiID, S.SarkiAdi, S.Sure, S.YayinTarihi, ART.SanatciIsmi
            FROM 
                FavoriSarkilar F
            JOIN 
                Sarki S ON F.SarkiID = S.SarkiID
            JOIN 
                Sanatci ART ON S.SanatciID = ART.SanatciID
            WHERE 
                F.KullaniciID = %s
        """
        cur.execute(query, (user_id,))
        result = cur.fetchall()
        print("Log: Song Service - Favorite songs = ", result, "User ID = ", user_id)
        cur.close()
        return result
