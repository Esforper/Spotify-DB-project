from flask_mysqldb import MySQL

class RoleService:
    def __init__(self, mysql: MySQL):
        self.mysql = mysql

    # ✅ Check if a user exists
    def user_exists(self, username):
        cur = self.mysql.connection.cursor()
        try:
            cur.execute("SELECT * FROM Kullanici WHERE Isim = %s;", (username,))
            user = cur.fetchone()
            return user
        except Exception as e:
            print(f"Error checking if user exists: {e}")
            return None
        finally:
            cur.close()

    # ✅ Delete user's role
    def delete_user_role(self, username):
        cur = self.mysql.connection.cursor()
        try:
            cur.execute("UPDATE Kullanici SET Rol = NULL WHERE Isim = %s;", (username,))
            self.mysql.connection.commit()
        except Exception as e:
            print(f"Error deleting user role: {e}")
            raise
        finally:
            cur.close()

    # ✅ Update user's role and email
    def update_user_role(self, username, email, role):
        cur = self.mysql.connection.cursor()
        try:
            cur.execute("""
                UPDATE Kullanici 
                SET Eposta = %s, Rol = %s 
                WHERE Isim = %s;
            """, (email, role, username))
            self.mysql.connection.commit()
        except Exception as e:
            print(f"Error updating user role: {e}")
            raise
        finally:
            cur.close()

    # ✅ Add a new user with a role
    def add_new_user(self, username, email, password, role):
        cur = self.mysql.connection.cursor()
        try:
            cur.execute("""
                INSERT INTO Kullanici (Isim, Eposta, Sifre, UyelikTarihi, Rol) 
                VALUES (%s, %s, %s, CURDATE(), %s);
            """, (username, email, password, role))
            self.mysql.connection.commit()
        except Exception as e:
            print(f"Error adding new user: {e}")
            raise
        finally:
            cur.close()

    # ✅ Retrieve all users
    def get_all_users(self):
        cur = self.mysql.connection.cursor()
        try:
            cur.execute("SELECT Isim, Eposta, Rol FROM Kullanici;")
            users = cur.fetchall()
            return users
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []
        finally:
            cur.close()