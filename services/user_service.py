class UserService:
    def __init__(self):
        # Geçici kullanıcı verileri
        self.users = {
            "admin": {"password": "password", "role": "Admin"},
            "user1": {"password": "pass123", "role": "User"},
            "emir": {"password": "mypassword", "role": "Artist"}
        }
        # Aktif kullanıcıları tutmak için bir set
        self.active_users = set()

    def validate_user(self, username, password, role):
        """Kullanıcı doğrulama."""
        user = self.users.get(username)
        if user and user['password'] == password and user['role'] == role:
            self.active_users.add(username)  # Kullanıcıyı aktif olarak işaretle
            return user  # Döndürülen kullanıcı objesi burada

        return None

    def logout_user(self, username):
        """Kullanıcıyı aktif listesinden çıkar."""
        self.active_users.discard(username)

    def get_user(self, username):
        """Kullanıcı bilgilerini döndür."""
        return self.users.get(username)  # Bu metodu ekledik

    def is_user_active(self, username):
        """Kullanıcının aktif olup olmadığını kontrol et."""
        return username in self.active_users