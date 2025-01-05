from flask_mysqldb import MySQL
import MySQLdb.cursors

class ArtistService:
    def __init__(self, mysql: MySQL):
        self.mysql = mysql
        
    def add_favorite_artist(self,user_id, artist_id):
        cur = self.mysql.connection.cursor()
        cur.execute(
            "INSERT INTO FavoriSanatcilar (KullaniciID, SanatciID) VALUES (%s, %s)",
            (user_id, artist_id)
        )
        cur.commit()
        
    def search_artist_by_query(self, query):
        cur = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            SELECT SanatciID, SanatciIsmi, Biyografi
            FROM Sanatci
            WHERE LOWER(SanatciIsmi) LIKE %s
        """, ('%' + query + '%',))  # Sanatçı ismine göre arama yapılır
        artists = cur.fetchall()
        print(artists)
        cur.close()
        return artists    