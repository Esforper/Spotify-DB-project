from flask_mysqldb import MySQL
import MySQLdb.cursors


class PlaylistService:
    def __init__(self,mysql: MySQL):
        self.mysql = mysql
        
    def get_playlists(self,user_id):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM CalmaListesi WHERE KullaniciID = %s", (user_id,))
        playlists = cur.fetchall()
        cur.close()
        return playlists
    
    def get_playlist_songs(self,playlist_id):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Sarki WHERE SarkiID IN (SELECT SarkiID FROM CalmaListesi_Sarkilar WHERE CalmaListesiID = %s)", (playlist_id,))
        songs = cur.fetchall()
        cur.close()
        return songs
    
    def create_playlist(self, name, user_id):
        cur = self.mysql.connection.cursor()
        cur.execute("INSERT INTO CalmaListesi (CalmaListesiAdi, KullaniciID) VALUES (%s, %s)", (name, user_id))
        self.mysql.connection.commit()
        cur.close()
        
    def delete_playlist(self, playlist_id):
        cur = self.mysql.connection.cursor()
        cur.execute("DELETE FROM CalmaListesi WHERE CalmaListesiID = %s", (playlist_id,))
        cur.execute("DELETE FROM CalmaListesi_Sarkilar WHERE CalmaListesiID = %s", (playlist_id,))
        self.mysql.connection.commit()
        cur.close()        
        
    def delete_song_from_playlist(self, playlist_id, song_id):
        cur = self.mysql.connection.cursor()
        cur.execute("""
            DELETE FROM CalmaListesi_Sarkilar
            WHERE CalmaListesiID = %s AND SarkiID = %s
        """, (playlist_id, song_id))
        self.mysql.connection.commit()
        cur.close()
        
        
    def get_playlist_by_id(self, playlist_id):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM CalmaListesi WHERE CalmaListesiID = %s", (playlist_id,))
        playlist = cur.fetchone()
        cur.close()
        return playlist
    
    def search_playlists_by_query(self, query):
        cur = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            SELECT CalmaListesiID, CalmaListesiAdi, KullaniciID 
            FROM CalmaListesi
            WHERE LOWER(CalmaListesiAdi) LIKE %s
        """, ('%' + query + '%',))  # Playlist adı üzerinden arama
        playlists = cur.fetchall()
        cur.close()
        return playlists

