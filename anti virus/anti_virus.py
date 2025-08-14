#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import random
import time
import threading
import sys

try:
    import winsound
except:
    winsound = None

SUSPICIOUS_FILES = [
    r"C:\Windows\System32\drivers\kbdclass.sys",
    r"C:\Users\Public\Videos\codec_patch.dll",
    r"C:\ProgramData\Steam\cache\steam_config.tmp",
    r"C:\Users\%USERNAME%\AppData\Local\Temp\svchost64.tmp",
    r"/usr/lib/python3.10/site-packages/pip/_internal/__init__.py",
    r"/etc/ssh/ssh_config.bak",
    r"/home/user/.cache/.X11-tmp.sock",
    r"C:\Windows\explorer_cache\thumbs.db",
    r"D:\Games\PUBG\Engine\Binaries\Win64\BuildCache.tmp",
    r"C:\Users\%USERNAME%\Documents\secret_pass.txt",
]

MALWARE_NAMES = [
    "RAT.Backdoor.ZeusX",
    "Trojan.Injector.Red",
    "Keylogger.DarkEye",
    "Worm.AutoRun.Ghost",
    "Spy.Agent.Cerberus",
    "Adware.PUA.GhostPop",
    "Rootkit.ShadowHive",
]

WARNINGS = [
    "Yetkisiz ağ trafiği tespit edildi",
    "Bilinmeyen işlem davranışı",
    "Bellek enjekte girişimi",
    "Sürekli ekran okuma isteği",
    "Şüpheli zamanlanmış görev",
]

FAKE_IPS = [f"{random.randint(12,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}" for _ in range(100)]

class PanicRAT:
    def __init__(self, root):
        self.root = root
        self.root.title("SECURITY ALERT")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")
        self.root.bind("<Escape>", lambda e: self.safe_exit())

        self.header = tk.Label(root, text="CRITICAL SECURITY ALERT", font=("Consolas", 32, "bold"), fg="#ff3b3b", bg="black")
        self.header.pack(pady=20)

        self.sub = tk.Label(root, text="Şüpheli aktivite tespit edildi. Sistem taraması başlatılıyor...", font=("Consolas", 18), fg="#ff9e9e", bg="black")
        self.sub.pack()

        self.log = tk.Text(root, height=20, width=120, bg="#0b0b0b", fg="#e6e6e6", insertbackground="white", font=("Consolas", 12))
        self.log.pack(pady=10)
        self.log.configure(state="disabled")

        self.progress_label = tk.Label(root, text="Tarama ilerlemesi: 0%", font=("Consolas", 14), fg="#cccccc", bg="black")
        self.progress_label.pack(pady=(10,0))
        self.progress = ttk.Progressbar(root, orient="horizontal", length=800, mode="determinate")
        self.progress.pack(pady=5)

        self.bottom_warning = tk.Label(root, text="", font=("Consolas", 16, "bold"), fg="#ff3b3b", bg="black")
        self.bottom_warning.pack(pady=10)

        self.stop_flag = False
        self.thread = threading.Thread(target=self.fake_scan, daemon=True)
        self.thread.start()

    def log_write(self, text):
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")
        self.root.update_idletasks()

    def safe_exit(self):
        self.stop_flag = True
        self.root.destroy()

    def fake_scan(self):
        self.log_write("[*] Güvenlik servisi başlatılıyor...")
        time.sleep(0.6)
        self.log_write("[*] Bellek imza veri tabanı yükleniyor...")
        time.sleep(0.6)
        self.log_write("[*] Davranışsal analiz motoru aktif...")
        time.sleep(0.6)

        total_steps = 100
        for i in range(total_steps + 1):
            if self.stop_flag: return
            if random.random()<0.3: self.log_write(f"[SCAN] Dosya inceleniyor: {random.choice(SUSPICIOUS_FILES)}")
            if random.random()<0.25: self.log_write(f"[WARN] {random.choice(WARNINGS)}")
            if random.random()<0.28: self.log_write(f"[NET] {random.choice(MALWARE_NAMES)} → {random.choice(FAKE_IPS)} ile bağlantı kuruluyor...")
            self.progress["value"] = i
            self.progress_label.config(text=f"Tarama ilerlemesi: {i}%")
            self.bottom_warning.config(text=random.choice([
                "Ağ trafiği inceleniyor...",
                "Yetkisiz işlem gözlemleniyor...",
                "Kimlik bilgisi erişim denemesi...",
                "Kritik sistem dosyaları doğrulanıyor...",
                "Uzak bağlantı tespit edildi...",
            ]))
            self.root.geometry(f"1200x800+{random.randint(0,50)}+{random.randint(0,50)}")
            if winsound and random.random()<0.05:
                winsound.Beep(800 + i, 150)
            time.sleep(0.05)

        self.log_write("\n[!] Kritik: Davranışsal anormallik eşik değeri aşıldı.")
        self.log_write("[!] Uzak erişim aktivitesi benzeri belirtiler tespit edildi.")
        self.log_write("[!] Sistem bütünlüğü doğrulaması başarısız.")

        for sec in range(10,0,-1):
            if self.stop_flag: return
            self.bottom_warning.config(text=f"UYARI: Sistem {sec} saniye içinde kilitlenecek!")
            if winsound: winsound.Beep(1000+sec*50, 200)
            time.sleep(0.8)

        self.show_bsod()

    def show_bsod(self):
        bsod = tk.Toplevel()
        bsod.attributes("-fullscreen", True)
        bsod.configure(bg="#0000AA")
        
        tk.Label(bsod, text=(
            "A problem has been detected and Windows has been shut down to prevent damage to your computer.\n\n"
            "Technical information:\n"
            "*** STOP: 0x0000007B (0xFFFFF880009A97E8, 0xFFFFFFFFC0000034)\n"
            "Collecting data for crash dump...\n"
            "Initializing disk for crash dump...\n"
            "Beginning dump of physical memory..."
        ), font=("Consolas",16), fg="white", bg="#0000AA", justify="left").pack(padx=50, pady=50, anchor="w")
        
        tk.Label(bsod, text="😂 TROLLED! Bilgisayarın %100 güvenli 😎", font=("Consolas", 32, "bold"), fg="yellow", bg="#0000AA").place(relx=0.5, rely=0.5, anchor="center")
        
        bsod.bind("<Escape>", lambda e: sys.exit())
        bsod.mainloop()

def main():
    root = tk.Tk()
    try: ttk.Style().theme_use("clam")
    except: pass
    PanicRAT(root)
    root.mainloop()

if __name__=="__main__":
    main()
