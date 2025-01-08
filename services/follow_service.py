from flask_mysqldb import MySQL

class FollowService:
    def __init__(self, mysql: MySQL):
        self.mysql = mysql

    def follow_artist(self, user_id, artist_id):
        cur = self.mysql.connection.cursor()
        cur.execute("""
            INSERT INTO Takip (TakipEdenKullaniciID, TakipEdilenSanatciID) 
            VALUES (%s, %s)
        """, (user_id, artist_id))
        self.mysql.connection.commit()
        cur.close()

    def unfollow_artist(self, user_id, artist_id):
        cur = self.mysql.connection.cursor()
        cur.execute("""
            DELETE FROM Takip 
            WHERE TakipEdenKullaniciID = %s AND TakipEdilenSanatciID = %s
        """, (user_id, artist_id))
        self.mysql.connection.commit()
        cur.close()

    def is_following(self, user_id, artist_id):
        cur = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            SELECT * FROM Takip 
            WHERE TakipEdenKullaniciID = %s AND TakipEdilenSanatciID = %s
        """, (user_id, artist_id))
        result = cur.fetchone()
        cur.close()
        return result is not None
