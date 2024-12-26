CREATE DATABASE Spotify_DB_Project;
USE Spotify_DB_Project;

-- Kullanıcı Tablosu
CREATE TABLE Kullanici (
    KullaniciID INT PRIMARY KEY AUTO_INCREMENT,
    Isim VARCHAR(100) NOT NULL,
    Eposta VARCHAR(100) UNIQUE NOT NULL,
    Sifre VARCHAR(100) NOT NULL,
    UyelikTarihi DATE NOT NULL,
    Rol ENUM('Dinleyici', 'Sanatçı') NOT NULL
);

-- Sanatçı Tablosu
CREATE TABLE Sanatci (
    SanatciID INT PRIMARY KEY AUTO_INCREMENT,
    KullaniciID INT NOT NULL,
    SanatciIsmi VARCHAR(100) NOT NULL,
    Biyografi TEXT,
    FOREIGN KEY (KullaniciID) REFERENCES Kullanici(KullaniciID)
);

-- Yönetici Tablosu
CREATE TABLE Yonetici (
    YoneticiID INT PRIMARY KEY AUTO_INCREMENT,
    Isim VARCHAR(100) NOT NULL,
    Eposta VARCHAR(100) UNIQUE NOT NULL,
    Sifre VARCHAR(100) NOT NULL
);

-- Sosyal Medya Linkleri Tablosu
CREATE TABLE SosyalMedyaLinkleri (
    LinkID INT PRIMARY KEY AUTO_INCREMENT,
    SanatciID INT NOT NULL,
    Platform VARCHAR(100) NOT NULL,
    URL VARCHAR(100) NOT NULL,
    FOREIGN KEY (SanatciID) REFERENCES Sanatci(SanatciID)
);


-- Tür Tablosu
CREATE TABLE Tur (
    TurID INT PRIMARY KEY AUTO_INCREMENT,
    TurAdi VARCHAR(100) NOT NULL,
    Aciklama TEXT
);

-- Albüm Tablosu
CREATE TABLE Album (
    AlbumID INT PRIMARY KEY AUTO_INCREMENT,
    AlbumAdi VARCHAR(100) NOT NULL,
    YayinTarihi DATE NOT NULL,
    TurID INT NOT NULL,
    SanatciID INT NOT NULL,
    FOREIGN KEY (TurID) REFERENCES Tur(TurID),
    FOREIGN KEY (SanatciID) REFERENCES Sanatci(SanatciID)
);


-- Şarkı Tablosu
CREATE TABLE Sarki (
    SarkiID INT PRIMARY KEY AUTO_INCREMENT,
    SarkiAdi VARCHAR(255) NOT NULL,
    Sure TIME NOT NULL,
    YayinTarihi DATE,
    TurID INT,
    AlbumID INT,
    SanatciID INT NOT NULL,
    FOREIGN KEY (TurID) REFERENCES Tur(TurID),
    FOREIGN KEY (AlbumID) REFERENCES Album(AlbumID),
    FOREIGN KEY (SanatciID) REFERENCES Sanatci(SanatciID)
);

 -- Çalma Listesi Tablosu
CREATE TABLE CalmaListesi (
    CalmaListesiID INT PRIMARY KEY AUTO_INCREMENT,
    CalmaListesiAdi VARCHAR(100) NOT NULL,
    KullaniciID INT NOT NULL,
    FOREIGN KEY (KullaniciID) REFERENCES Kullanici(KullaniciID)
);

-- Çalma Listesi - Şarkılar Ara Tablosu
CREATE TABLE CalmaListesi_Sarkilar (
    CalmaListesiSarkilarID INT PRIMARY KEY AUTO_INCREMENT,
    CalmaListesiID INT NOT NULL,
    SarkiID INT NOT NULL,
    FOREIGN KEY (CalmaListesiID) REFERENCES CalmaListesi(CalmaListesiID),
    FOREIGN KEY (SarkiID) REFERENCES Sarki(SarkiID)
);

-- Favori Sanatçlar TablosuCalmaListesi_Sarkilar
CREATE TABLE FavoriSanatcilar (
    FavoriID INT PRIMARY KEY AUTO_INCREMENT,
    KullaniciID INT NOT NULL,
    SanatciID INT NOT NULL,
    FOREIGN KEY (KullaniciID) REFERENCES Kullanici(KullaniciID),
    FOREIGN KEY (SanatciID) REFERENCES Sanatci(SanatciID)
);

-- Favori Şarkılar Tablosu
CREATE TABLE FavoriSarkilar (
    FavoriID INT PRIMARY KEY AUTO_INCREMENT,
    KullaniciID INT NOT NULL,
    SarkiID INT NOT NULL,
    FOREIGN KEY (KullaniciID) REFERENCES Kullanici(KullaniciID),
    FOREIGN KEY (SarkiID) REFERENCES Sarki(SarkiID)
);

-- Takip Tablosu
CREATE TABLE Takip (
    TakipID INT PRIMARY KEY AUTO_INCREMENT,
    TakipEdenKullaniciID INT NOT NULL,
    TakipEdilenSanatciID INT NOT NULL,
    FOREIGN KEY (TakipEdenKullaniciID) REFERENCES Kullanici(KullaniciID),
    FOREIGN KEY (TakipEdilenSanatciID) REFERENCES Sanatci(SanatciID)
);

-- Şarkı Yorumları Tablosu
CREATE TABLE SarkiYorumlari (
    YorumID INT PRIMARY KEY AUTO_INCREMENT,
    KullaniciID INT NOT NULL,
    SarkiID INT NOT NULL,
    İcerik TEXT NOT NULL,
    YorumTarihi DATE NOT NULL,
    FOREIGN KEY (KullaniciID) REFERENCES Kullanici(KullaniciID),
    FOREIGN KEY (SarkiID) REFERENCES Sarki(SarkiID)
);

-- Albüm Yorumları Tablosu
CREATE TABLE AlbumYorumlari (
    YorumID INT PRIMARY KEY AUTO_INCREMENT,
    KullaniciID INT NOT NULL,
    AlbumID INT NOT NULL,
    İcerik TEXT NOT NULL,
    YorumTarihi DATE NOT NULL,
    FOREIGN KEY (KullaniciID) REFERENCES Kullanici(KullaniciID),
    FOREIGN KEY (AlbumID) REFERENCES Album(AlbumID)
); 
