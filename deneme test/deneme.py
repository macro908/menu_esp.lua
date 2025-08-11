import os
import time
import random
import string
import sys
import winsound

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_red_blink(text, times=5):
    for _ in range(times):
        os.system('color 4')  # kırmızı
        print(text)
        time.sleep(0.5)
        clear_screen()
        time.sleep(0.2)
    os.system('color 7')  # normal renk

def random_string(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def glitch_text(text):
    glitch_chars = ['#', '@', '%', '&', '?', '!', '*']
    text_list = list(text)
    for _ in range(10):
        idx = random.randint(0, len(text_list) -1)
        text_list[idx] = random.choice(glitch_chars)
        sys.stdout.write('\r' + ''.join(text_list))
        sys.stdout.flush()
        time.sleep(0.2)
    print()

def matrix_effect(duration=5):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    end_time = time.time() + duration
    while time.time() < end_time:
        line = ''.join(random.choice(chars) for _ in range(80))
        print(line)
        time.sleep(0.05)
        clear_screen()

def beep_alert(times=3):
    os.system('color 4')  # kırmızı
    for _ in range(times):
        winsound.MessageBeep()
        print("!!! KRİTİK HATA: RAT ALARMI !!!")
        time.sleep(1)
        clear_screen()
        time.sleep(0.5)
    os.system('color 7')

def main():
    clear_screen()
    print("=== Sistem Taraması Başlatılıyor ===")
    time.sleep(2)

    for i in range(1, 6):
        print(f"[{i}] Dosya taranıyor...")
        time.sleep(0.5)

    print_red_blink("\n!!! TEHLİKE: RAT TESPİT EDİLDİ !!!")

    print("[!] IP adresi tespit ediliyor...")
    time.sleep(1.5)

    ips = ["185.92.0.1", "92.44.11.23", "144.12.92.4", "37.214.85.199"]
    users = ["Admin", "root", "Guest", "system32"]

    print(f"[+] Bağlantı sağlandı: {random.choice(ips)}")
    time.sleep(1)
    print(f"[+] Yetkisiz kullanıcı girişi: {random.choice(users)}")
    time.sleep(1.5)

    beep_alert()

    print("\nBulaşan dosya sayısı tespit ediliyor...")
    infected = random.randint(8, 25)
    for i in range(infected):
        fake_file = f"C:\\Users\\Admin\\Documents\\{random_string(8)}_{random_string(4)}.exe"
        print(f" - Enfekte dosya bulundu: {fake_file}")
        time.sleep(0.3)

    print("\n[!] RAT sistemi ele geçirdi!")
    time.sleep(1)

    glitch_text("Sistem çökmek üzere...")

    matrix_effect(7)

    print("\n[!] Tüm veriler dışarıya aktarılıyor...")
    for i in range(0, 101, 10):
        print(f"   İlerleme: %{i}")
        time.sleep(0.2)

    print("\n💀 Şaka yaptım! Bu sadece sahte bir antivirüs simülasyonu 😄")
    time.sleep(1)
    input("\nÇıkmak için Enter'a bas...")

if __name__ == "__main__":
    main()
