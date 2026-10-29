# Üretim araçları

- brand.py: marka kiti ve çizim yardımcıları (kod kutusu, tablo, Venn, rozet)
- carousels.py / reels.py: hafta 1 örnekleri, yeni içerikler için şablon
- music.py: telifsiz lo-fi altyapı üretir: python3 music.py cikti.wav SANIYE [seed]
- verify_sql.py: örnek sorguları SQLite'ta çalıştırma kalıbı

Videoya müzik ekleme:
ffmpeg -i video.mp4 -i muzik.wav -c:v copy -c:a aac -b:a 128k -af "volume=0.8,loudnorm=I=-18:TP=-1.5" -map 0:v -map 1:a cikti.mp4
