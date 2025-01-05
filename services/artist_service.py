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
        self.mysql.connection.commit()
        cur.close()
        
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
    
    def get_favorite_artists(self, user_id):
        cur = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = """
            SELECT 
                ART.SanatciID, ART.SanatciIsmi
            FROM 
                FavoriSanatcilar F
            JOIN 
                Sanatci ART ON F.SanatciID = ART.SanatciID
            WHERE 
                F.KullaniciID = %s
        """
        cur.execute(query, (user_id,))
        result = cur.fetchall()
        cur.close()
        return result
