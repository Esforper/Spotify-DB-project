-- Kullanıcı Ekleme
INSERT INTO Kullanici (Isim, Eposta, Sifre, UyelikTarihi, Rol)
VALUES 
('Ahmet Yılmaz', 'ahmet@example.com', '123456', '2024-12-12', 'Dinleyici'),
('Mehmet Kaya', 'mehmet@example.com', '654321', '2024-11-10', 'Dinleyici'),
('Ayşe Çelik', 'ayse@example.com', '123654', '2024-10-01', 'Dinleyici'),
('Fatma Öztürk', 'fatma@example.com', '321456', '2024-09-15', 'Dinleyici'),
('Ali Demir', 'ali@example.com', '654123', '2024-08-20', 'Dinleyici');

-- Tür Ekleme
INSERT INTO Tur (TurAdi, Aciklama) 
VALUES 
('Pop', 'Pop müzik türü'),
('Rock', 'Rock müzik türü'),
('Türk Sanat Müziği', 'Geleneksel Türk müziği'),
('Alternatif', 'Alternatif müzik türü'),
('Rap', 'Rap müzik türü');


-- Sanatçı Ekleme
INSERT INTO Sanatci (KullaniciID, SanatciIsmi, Biyografi)
VALUES 
(1, 'Tarkan', 'Türk pop müziğinin megastarı.'),
(2, 'Sezen Aksu', 'Minik Serçe lakaplı ünlü sanatçı.'),
(3, 'Cem Karaca', 'Türk rock müziğinin öncülerinden.'),
(4, 'Barış Manço', 'Türk müziğinin unutulmaz ismi.'),
(5, 'Ajda Pekkan', 'Türk pop müziğinin Süperstarı.'),
(6, 'Teoman', 'Türk alternatif rock sanatçısı.'),
(7, 'Ceza', 'Türk rap müziğinin önemli ismi.'),
(8, 'Zeki Müren', 'Türk sanat müziğinin efsanesi.'),
(9, 'Edis', 'Yeni nesil Türk pop sanatçısı.'),
(10, 'Gülşen', 'Popüler Türk pop sanatçısı.');


-- Şarkı Ekleme
INSERT INTO Sarki (SarkiAdi, Sure, YayinTarihi, TurID, SanatciID)
VALUES 
('Şımarık', '00:03:45', '1997-05-15', 1, 1),
('Kuzu Kuzu', '00:03:50', '2001-05-25', 1, 1),
('Dön Bebeğim', '00:04:05', '2003-05-25', 1, 1),
('İkimizin Yerine', '00:04:00', '2006-12-15', 1, 1),
('O’na Sor', '00:03:50', '2009-06-05', 1, 1),
('Sevdanın Son Vuruşu', '00:03:55', '2007-06-01', 1, 1),
('Beni Anlama', '00:04:00', '2005-03-12', 1, 1),
('Unut Beni', '00:04:00', '2005-03-12', 1, 1),
('Dön', '00:03:45', '2007-09-17', 1, 1),
('Kır Zincirlerini', '00:03:50', '1998-09-30', 1, 1),
('Gülümse', '00:04:10', '1984-03-20', 1, 2),
('Seni Yerler', '00:04:00', '1986-05-15', 1, 2),
('Haydi Gel Benimle Ol', '00:03:45', '2001-06-18', 1, 2),
('Kusura Bakma / Geçmişe Dayanamam', '00:03:50', '2011-04-05', 1, 2),
('İhanetten Geri Kalan', '00:04:00', '2009-07-08', 1, 2),
('Yansın İstanbul', '00:04:10', '1999-11-22', 1, 2),
('Rakkas', '00:04:00', '1980-06-30', 1, 2),
('Aşk', '00:04:20', '1995-03-14', 1, 2),
('Son Bakış', '00:04:05', '2014-12-01', 1, 2),
('Biliyorsun', '00:04:10', '2003-09-12', 1, 2),
('Ceviz Ağacı', '00:04:05', '1979-07-10', 2, 3),
('Resimdeki Gözyaşları', '00:04:00', '1980-10-01', 2, 3),
('Baba', '00:03:50', '1979-06-20', 2, 3),
('Islak Islak', '00:03:45', '1982-03-30', 2, 3),
('Ay Karanlık', '00:03:55', '1978-08-01', 2, 3),
('Bu Son Olsun', '00:04:00', '1985-05-20', 2, 3),
('Çökertme', '00:03:55', '1978-12-12', 2, 3),
('İstanbul', '00:03:50', '1981-09-15', 2, 3),
('Deniz Üstü Köpürür', '00:03:40', '1982-04-01', 2, 3),
('Anlatamıyorum', '00:04:05', '1979-02-12', 2, 3),
('Hal Hal', '00:04:05', '1981-05-10', 2, 4),
('Gülpembe', '00:03:50', '1972-12-20', 2, 4),
('Dağlar Dağlar', '00:04:10', '1972-08-05', 2, 4),
('Sarı Çizmeli Mehmet Ağa', '00:04:00', '1972-06-01', 2, 4),
('Eğri Eğri Doğru Doğru', '00:03:55', '1982-07-15', 2, 4),
('Bal Böceği', '00:03:50', '1974-11-10', 2, 4),
('Ben Bilirim', '00:04:00', '1981-03-01', 2, 4),
('Nerede', '00:04:05', '1983-01-20', 2, 4),
('Dönence', '00:04:10', '1981-11-15', 2, 4),
('Aynalı Kemer', '00:03:55', '1976-08-20', 2, 4),
('Kimler Geldi Kimler Geçti', '00:04:05', '1976-09-01', 1, 5),
('O Benim Dünyam', '00:03:50', '1980-05-20', 1, 5),
('Yaz Yaz Yaz', '00:03:45', '1983-05-01', 1, 5),
('Bambaşka Biri', '00:04:05', '1999-03-20', 1, 5),
('Hoş Gör Sen', '00:03:50', '1990-07-12', 1, 5),
('Arada Sırada', '00:03:55', '1991-11-15', 1, 5),
('Eğlen Güzelim', '00:03:45', '1977-06-01', 1, 5),
('Bir Günah Gibi', '00:04:00', '1991-09-01', 1, 5),
('Yakar Geçerim', '00:04:00', '2005-02-01', 1, 5),
('Kim Ne Derse Desin', '00:03:45', '1996-03-15', 1, 5),
('Gemiler', '00:04:05', '1997-03-01', 2, 6),
('Serseri', '00:03:50', '1998-08-10', 2, 6),
('Paramparça', '00:04:10', '1997-11-20', 2, 6),
('Renkli Rüyalar Oteli', '00:03:50', '2000-10-15', 2, 6),
('İstanbulda Sonbahar', '00:03:55', '1998-11-01', 2, 6),
('Sevdim Seni Bir Kere', '00:03:45', '2001-05-01', 2, 6),
('Kupa Kızı ve Sinek Valesi', '00:04:00', '2004-04-05', 2, 6),
('Aşk Kırıntıları', '00:04:05', '2000-06-20', 2, 6),
('Bana Öyle Bakma', '00:03:50', '2002-09-01', 2, 6),
('Napim Tabiatim Böyle', '00:03:55', '1997-10-01', 2, 6),
('Neyim Var Ki', '00:03:55', '2004-02-01', 3, 7),
('Holocaust', '00:04:05', '2004-03-10', 3, 7),
('Ben Ağlamazken', '00:03:50', '2004-04-25', 3, 7),
('Suspus', '00:04:00', '2004-11-15', 3, 7),
('Yerli Plaka', '00:04:10', '2004-03-01', 3, 7),
('Bu Rap Muharebe', '00:03:45', '2004-05-01', 3, 7),
('Medcezir', '00:03:50', '2006-06-10', 3, 7),
('Fark Var', '00:03:40', '2009-10-01', 3, 7),
('Panorama Harem', '00:04:00', '2004-03-15', 3, 7),
('Türk Marşı', '00:04:05', '2006-03-20', 3, 7),
('Şimdi Uzaklardasın', '00:04:00', '1960-04-01', 4, 8),
('Gitme Sana Muhtacım', '00:03:50', '1965-06-01', 4, 8),
('Gözlerin Doğuyor Gecelerime', '00:03:55', '1967-05-01', 4, 8),
('Bulamazsın', '00:03:40', '1967-09-01', 4, 8),
('Ah Bu Şarkıların Gözü Kör Olsun', '00:04:05', '1968-10-10', 4, 8),
('Ben Zeki Müren', '00:03:45', '1972-08-01', 4, 8),
('Bana Bir Aşk Masalından', '00:03:50', '1962-05-01', 4, 8),
('Elbet Bir Gün Buluşacağız', '00:03:55', '1973-09-01', 4, 8),
('Beni Terk Etme', '00:04:00', '1969-02-20', 4, 8),
('Sorma Ne Haldeyim', '00:04:10', '1964-12-01', 4, 8),
('Ân', '00:03:40', '2017-05-01', 1, 9),
('Arıyorum', '00:03:50', '2017-07-10', 1, 9),
('Dudak', '00:03:45', '2018-11-05', 1, 9),
('Benim Ol', '00:03:55', '2020-10-15', 1, 9),
('Çok Çok', '00:03:30', '2019-05-10', 1, 9),
('Ayyaş', '00:03:40', '2020-05-01', 1, 9),
('Azar Azar', '00:04:00', '2021-03-05', 1, 9),
('Buz Kırağı', '00:03:45', '2022-04-01', 1, 9),
('Martılar', '00:03:50', '2022-09-10', 1, 9),
('Olmamış Mı', '00:03:55', '2021-01-25', 1, 9),
('Yatcaz Kalkcaz Ordayım', '00:03:45', '2004-09-10', 1, 10),
('Bangır Bangır', '00:03:50', '2015-12-01', 1, 10),
('Önsöz', '00:03:40', '2009-07-01', 1, 10),
('Dillere Düşeceğiz Seninle', '00:03:55', '2014-05-15', 1, 10),
('Bir Taraf Seç', '00:04:00', '2004-02-15', 1, 10),
('Bir Fırt Çek', '00:03:50', '2011-06-01', 1, 10),
('Irgalamaz Beni', '00:03:40', '2012-10-20', 1, 10),
('Sarışınım', '00:03:55', '2013-03-15', 1, 10),
('Bir İhtimal Biliyorum', '00:03:45', '2008-11-01', 1, 10),
('Kardan Adam', '00:04:00', '2017-03-01', 1, 10);



-- albüm ekleme 
INSERT INTO Album (AlbumAdi, YayinTarihi, TurID, SanatciID)
VALUES 
('Ölürüm Sana', '1997-05-15', 1, 1),
('Kuzu Kuzu', '2001-05-25', 1, 1),
('Aacayipsin', '2003-07-01', 1, 1),
('Karma', '2009-06-05', 1, 1),
('Adimi Kalbine Yaz','2007-06-01', 1, 1),
('Gülümse', '1984-03-20', 1, 2),
('Düş Bahçeleri', '1986-05-15', 1, 2),
('Sen Ağlama', '2001-06-18', 1, 2),
('Kusura Bakma ', '2011-04-05', 1, 2),
('Biraz Pop Biraz Sen', '2009-07-08', 1, 2),
('Demo', '1999-11-22', 1, 2),
('Işik Doğudan Yükselir', '1980-06-30', 1, 2),
('Sezen Aksu Söylüyor','2014-12-01', 1, 2),
('Ağlamak Güzeldir','2003-09-12', 1, 2),
('Merhaba Gençler ve Her Zaman Genç Kalanlar', '1979-07-10', 2, 3),
('Resimdeki Gözyaşları', '1980-10-01', 2, 3),
('Nem Kaldi', '1979-06-20', 2, 3),
('Nerde Kalmiştik', '1982-03-30', 2, 3),
('Cemaz-Ül-Evvel', '1985-05-20', 2, 3),
('Ankara','1982-04-01', 2, 3),
('Hal Hal', '1981-05-10', 2, 4),
('Sözüm Meclisten Dişari',  '1972-12-20', 2, 4),
('Dağlar Dağlar',  '1972-08-05', 2, 4),
('Mançoloji', '1972-06-01', 2, 4),
('Eğri Eğri Doğru Doğru', '1982-07-15', 2, 4),
('Müsadenizle Çocuklar', '1974-11-10', 2, 4),
('Mançoloji 2', '1981-03-01', 2, 4),
('Değmesin Yağli Boya', '1983-01-20', 2, 4), 
('Ajda', '1976-09-01', 1, 5),
('Ajda Pekkan ve Beş Yil Önce On Yil Sonra', '1980-05-20', 1, 5),
('Ajda 1990',  '1983-05-01', 1, 5),
('Süperstar 2', '1999-03-20', 1, 5),
('Hoş Gör Sen', '1990-07-12', 1, 5),
('Farkin Bu', '1991-11-15', 1, 5),
('Eğlen Güzelim', '1977-06-01', 1, 5),
('Süperstar 83 ',  '1991-09-01', 1, 5),
('Süperstar', '1996-03-15', 1, 5),
('O', '1997-03-01', 2, 6),
('Eski Bir Rüya Uğruna', '1998-08-10', 2, 6),
('Onyedi', '1997-11-20', 2, 6),
('Renkli Rüyalar Oteli', '2000-10-15', 2, 6),
('Gönülçelen', '1998-11-01', 2, 6),
('Teo','2004-04-05', 2, 6),
('Aşk ve Gurur', '2002-09-01', 2, 6),
('Rapstar', '2004-02-01', 3, 7),
('Suspus', '2004-11-15', 3, 7),
('Yerli Plaka', '2004-03-01', 3, 7),
('Medcezir', '2006-06-10', 3, 7),
('Türk Marşı', '2006-03-20', 3, 7),
('Eskimeyen Dost', '1960-04-01', 4, 8),
('Gitme Sana Muhtacım', '1965-06-01', 4, 8),
('Gözlerin Doğuyor Gecelerime', '1967-05-01', 4, 8),
('Bir Sevgi İstiyorum', '1967-09-01', 4, 8),
('Zirvedeki Şarkilar',  '1968-10-10', 4, 8),
('Dünden bugüne 4', '1962-05-01', 4, 8),
('Dünden Bugüne 5', '1973-09-01', 4, 8),
('Zeki Müren Klasikleri Vol. 5', '1969-02-20', 4, 8),
('Batmayan Güneş',  '1964-12-01', 4, 8),
('Ân', '2017-05-01', 1, 9),
('Arıyorum','2017-07-10', 1, 9),
('Dudak', '2018-11-05', 1, 9),
('Olmamiş Mi', '2020-10-15', 1, 9),
('Ayyaş', '2020-05-01', 1, 9),
('Azar Azar','2021-03-05', 1, 9),
('Yildiz Tilbenin Yildizli Şarkilari Volume 2', '2022-04-01', 1, 9),
('Martılar', '2022-09-10', 1, 9),
('Beni durdursan Mi', '2004-09-10', 1, 10),
('Bangır Bangır', '2015-12-01', 1, 10),
('Önsöz', '2009-07-01', 1, 10),
('Of... Of...', '2013-03-15', 1, 10),
('Bir İhtimal Biliyorum','2008-11-01', 1, 10);


-- çalma listesi ekleme
INSERT INTO CalmaListesi (CalmaListesiAdi, KullaniciID)
VALUES ('Sabah Enerjisi', 1);

-- çalma listesine şarkı ekleme
INSERT INTO CalmaListesi_Sarkilar (CalmaListesiID, SarkiID)
VALUES (1, 1);


-- şarkıya yorum ekleme
INSERT INTO SarkiYorumlari (KullaniciID, SarkiID, Icerik, YorumTarihi)
VALUES (1, 1, 'Harika bir şarkı!', '2023-12-13');

-- albüme yorum ekleme
INSERT INTO AlbumYorumlari (KullaniciID, AlbumID, Icerik, YorumTarihi)
VALUES (1, 1, 'Bu albümü çok sevdim!', '2023-12-13');

-- favorilere şarkı ekleme
INSERT INTO FavoriSarkilar (KullaniciID, SarkiID)
VALUES (1, 1);

-- favorilere sanatçı ekleme
INSERT INTO FavoriSanatcilar (KullaniciID, SanatciID)
VALUES (1, 1);

-- takip etme
INSERT INTO Takip (TakipEdenKullaniciID, TakipEdilenSanatciID)
VALUES (1, 1);

-- kullanıcıların tüm çalma listelerini görüntüle
SELECT Kullanici.Isim AS KullaniciAdi, CalmaListesi.CalmaListesiAdi
FROM Kullanici
JOIN CalmaListesi ON Kullanici.KullaniciID = CalmaListesi.KullaniciID;

-- bir albümdeki şarkıları listele
SELECT Sarki.SarkiAdi, Sarki.Sure
FROM Sarki
WHERE Sarki.SarkiID = 1;

-- bir kullanıcının favori şarkılarını listele
SELECT Sarki.SarkiAdi
FROM FavoriSarkilar
JOIN Sarki ON FavoriSarkilar.SarkiID = Sarki.SarkiID
WHERE FavoriSarkilar.KullaniciID = 1;

-- bir kullanıcının favori sanatçılarını listele
SELECT Sanatci.SanatciIsmi
FROM FavoriSanatcilar
JOIN Sanatci ON FavoriSanatcilar.SanatciID = Sanatci.SanatciID
WHERE FavoriSanatcilar.KullaniciID = 1;

-- bir şarkıya yapılan yorumları listele
SELECT Kullanici.Isim AS Yorumcu, SarkiYorumlari.Icerik, SarkiYorumlari.YorumTarihi
FROM SarkiYorumlari
JOIN Kullanici ON SarkiYorumlari.KullaniciID = Kullanici.KullaniciID
WHERE SarkiYorumlari.SarkiID = 1;


-- bir albüme yapılan yorumları listele
SELECT Kullanici.Isim AS Yorumcu, AlbumYorumlari.Icerik, AlbumYorumlari.YorumTarihi
FROM AlbumYorumlari
JOIN Kullanici ON AlbumYorumlari.KullaniciID = Kullanici.KullaniciID
WHERE AlbumYorumlari.AlbumID = 1;

-- takip edilen sanatçıları listele
SELECT Sanatci.SanatciIsmi
FROM Takip
JOIN Sanatci ON Takip.TakipEdilenSanatciID = Sanatci.SanatciID
WHERE Takip.TakipEdenKullaniciID = 1;

--  kullanıcı ismini güncelle
UPDATE Kullanici
SET Isim = 'Mehmet Yılmaz'
WHERE KullaniciID = 1;


-- çalma listesi ismini güncelle
UPDATE CalmaListesi
SET CalmaListesiAdi = 'Enerjik Sabahlar'
WHERE CalmaListesiID = 1;

-- bir şarkıyı favorilerden sil
DELETE FROM FavoriSarkilar
WHERE KullaniciID = 1 AND SarkiID = 1;

-- bir kullanıcının çalma listesini sil
DELETE FROM CalmaListesi
WHERE KullaniciID = 1 AND CalmaListesiID = 1;


-- bir yorum sil
DELETE FROM SarkiYorumlari
WHERE YorumID = 1;











