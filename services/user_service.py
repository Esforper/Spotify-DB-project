from flask_mysqldb import MySQL
import MySQLdb.cursors

class UserService:
    
    def __init__(self, mysql: MySQL):
        self.mysql = mysql
    
    def validate_user(self, email, password, role):
        """
        Veritabanından kullanıcı doğrulama.
        """
        print("User bilgileri", email, password, role)
        cur = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if role == "Yönetici":
            cur.execute(
                "SELECT * FROM Yonetici WHERE Eposta = %s AND Sifre = %s",
                (email, password)
            )
        else:
            cur.execute(
                "SELECT * FROM Kullanici WHERE Eposta = %s AND Sifre = %s AND Rol = %s",
                (email, password, role)
            )
        user = cur.fetchone()
        cur.close()
        return user

    def create_user(self, name, email, password, role):
        """
        Yeni bir kullanıcı oluştur.
        """
        try:
            cur = self.mysql.connection.cursor()
            cur.execute(
                "INSERT INTO Kullanici (Isim, Eposta, Sifre, UyelikTarihi, Rol) VALUES (%s, %s, %s, CURDATE(), %s)",
                (name, email, password, role)
            )
            self.mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
        
    def create_admin(self, name, email, password):
        """
        Yeni bir yönetici oluştur.
        """
        try:
            cur = self.mysql.connection.cursor()
            cur.execute(
                "INSERT INTO Yonetici (Isim, Eposta, Sifre) VALUES (%s, %s, %s)",
                (name, email, password)
            )
            self.mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error creating admin: {e}")
            return False


    def logout_user(self, email):
        """
        Çıkış işlemi (veritabanı aktiflik durumu tutuluyorsa burada işlenebilir).
        """
        pass  # Bu örnekte sadece frontend oturumunu temizleyeceğiz.
    

    def get_user(self, email, role):
        """
        Belirli bir kullanıcının bilgilerini getir.
        """
        cur = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if role == "Yönetici":
            cur.execute("SELECT * FROM Yonetici WHERE Eposta = %s", (email,))
        else:
            cur.execute("SELECT * FROM Kullanici WHERE Eposta = %s", (email,))
        user = cur.fetchone()
        cur.close()
        return user

    def is_user_active(self, email):
        """
        Kullanıcının aktif olup olmadığını kontrol et.
        Eğer aktiflik durumu veritabanında tutuluyorsa sorgulanabilir.
        """
        # Örneğin, aktif kullanıcılar tablosunda kontrol yapılabilir.
        return True