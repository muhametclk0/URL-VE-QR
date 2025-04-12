import subprocess
import sys

def pip_yukle(paket):
    try:
        __import__(paket)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", paket])

pip_yukle("pyshorteners")
pip_yukle("qrcode")
pip_yukle("Pillow")

import pyshorteners
import qrcode
from PIL import Image
import os

def kisa_url_olustur(url, servis='tinyurl'):
    s = pyshorteners.Shortener()
    try:
        if servis == 'tinyurl':
            return s.tinyurl.short(url)
        elif servis == 'isgd':
            return s.isgd.short(url)
        elif servis == 'dagd':
            return s.dagd.short(url)
        elif servis == 'chilpit':
            return s.chilpit.short(url)
        else:
            return "Geçersiz servis."
    except Exception as e:
        return f"Hata: {e}"

def qr_olustur(url, dosya_adi):
    img = qrcode.make(url)
    path = os.path.join("qr_kodlar", dosya_adi)
    os.makedirs("qr_kodlar", exist_ok=True)
    img.save(path)
    print(f"QR kod kaydedildi: {path}")

def servis_sec():
    print("\nKullanılacak servis:")
    print("1. TinyURL")
    print("2. is.gd")
    print("3. da.gd")
    print("4. chilpit")
    secim = input("Seçiminiz (varsayılan 1): ").strip()
    return {'1': 'tinyurl', '2': 'isgd', '3': 'dagd', '4': 'chilpit'}.get(secim, 'tinyurl')

def tek_url_kisalt():
    url = input("\nKısaltılacak URL: ").strip()
    if not url:
        print("URL boş olamaz.")
        return
    servis = servis_sec()
    kisa = kisa_url_olustur(url, servis)
    print(f"Kısaltılmış URL: {kisa}")
    kaydet(url, kisa, servis)
    qr_olustur(kisa, f"qr_{servis}_{hash(url)%10000}.png")
    print("İşlem tamamlandı, menüye dönülüyor...")

def coklu_url_kisalt():
    print("\nÇıkmak için boş bırak.")
    while True:
        url = input("URL: ").strip()
        if not url:
            print("Çoklu işlem tamamlandı, menüye dönülüyor...")
            break
        servis = servis_sec()
        kisa = kisa_url_olustur(url, servis)
        print(f"Kısaltıldı ({servis}): {kisa}")
        kaydet(url, kisa, servis)
        qr_olustur(kisa, f"qr_{servis}_{hash(url)%10000}.png")

def kaydet(orijinal, kisa, servis):
    with open("kisaltilmis_url_listesi.txt", "a", encoding="utf-8") as f:
        f.write(f"{orijinal} -> {kisa} [{servis}]\n")

def menu_goster():
    print("\n--- URL Kısaltıcı + QR Kod Üretici ---")
    print("1. Tek URL kısalt ve QR oluştur")
    print("2. Çoklu URL kısalt ve QR oluştur")
    print("3. Çıkış")

def baslat():
    while True:
        menu_goster()
        secim = input("Seçim yap: ").strip()
        if secim == '1':
            tek_url_kisalt()
        elif secim == '2':
            coklu_url_kisalt()
        elif secim == '3':
            print("Çıkılıyor...")
            break
        else:
            print("Geçersiz seçim.")

baslat()

#ytr3so