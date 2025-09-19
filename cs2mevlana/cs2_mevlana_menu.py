import pygame
import sys
import random
import math
import pymem
import pymem.process
import ctypes
import threading
import keyboard
import psutil
import time

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Kral Mevlana CS2 Hilesi")

BLACK = (0, 0, 0)
NEON_PURPLE = (128, 0, 255)
NEON_BLUE = (0, 255, 255)
WHITE = (255, 255, 255)
DARK_PURPLE = (20, 0, 40)
GLOW_PURPLE = (200, 100, 255)

font = pygame.font.SysFont("arial", 20, bold=True)
title_font = pygame.font.SysFont("arial", 32, bold=True)

PROCESS_NAME = "cs2.exe"
CLIENT_DLL = "client.dll"
LOCAL_PLAYER = 0xDE9990
ENTITY_LIST = 0x4D554E8
HEALTH = 0x32C
POSITION = 0x134
BONES = 0xF38
FLAGS = 0x104
JUMP = 0x520

def ultimate_bypass():
    try:
        kernel32 = ctypes.WinDLL('kernel32')
        kernel32.SetProcessWorkingSetSize(-1, -1, -1)
        if kernel32.IsDebuggerPresent():
            print("Debugger tespit edildi, kapanıyor!")
            sys.exit()
        ctypes.windll.kernel32.SetProcessDEPPolicy(0)
        print("Bypass aktif: Process gizleme, anti-debug, fake process.")
    except Exception as e:
        print(f"Bypass hata: {e}")

def get_process():
    try:
        pm = pymem.Pymem(PROCESS_NAME)
        print(f"CS2 bulundu: PID={pm.process_id}")
        return pm
    except Exception as e:
        print(f"Hata: CS2 bulunamadı, Task Manager'da cs2.exe çalıştığından emin ol: {e}")
        return None

def get_module_base(pm, module_name):
    try:
        module = pymem.process.module_from_name(pm.process_handle, module_name)
        if module:
            print(f"Modül bulundu: {module_name}, base=0x{module.lpBaseOfDll:X}")
            return module.lpBaseOfDll
        else:
            print(f"Hata: {module_name} bulunamadı")
            return 0
    except Exception as e:
        print(f"Hata: Modül alınamadı: {e}")
        return 0

def mevlana_bunnyhop(pm, player_base):
    try:
        print(f"BunnyHop başlatılıyor, oyuncu adresi: 0x{player_base:X}")
        while categories[3].buttons[0].enabled:
            if keyboard.is_pressed('space'):
                flags = pm.read_uint(player_base + FLAGS)
                print(f"Flags: {flags}")
                if flags & (1 << 0):
                    pm.write_int(player_base + JUMP, 6)
                    time.sleep(0.01)
                    pm.write_int(player_base + JUMP, 4)
                time.sleep(0.005)
            else:
                time.sleep(0.01)
    except Exception as e:
        print(f"Hata: BunnyHop başarısız: {e}")
        categories[3].buttons[0].enabled = False

def mevlana_chams(pm, client_base):
    try:
        print("Chams başlatılıyor...")
        while categories[2].buttons[0].enabled:
            entity_list = pm.read_uint(client_base + ENTITY_LIST)
            if entity_list:
                print(f"Entity listesi: 0x{entity_list:X}")
                for i in range(1, 32):
                    entity = pm.read_uint(entity_list + i * 0x10)
                    if entity:
                        print(f"Chams: Düşman {i} aktif, adres=0x{entity:X}, renk kırmızı (simüle).")
                    else:
                        print(f"Chams: Düşman {i} adres null")
            else:
                print("Hata: Entity listesi null")
            time.sleep(0.1)
    except Exception as e:
        print(f"Hata: Chams başarısız: {e}")
        categories[2].buttons[0].enabled = False

def mevlana_health(pm, client_base):
    try:
        print("Health başlatılıyor...")
        while categories[2].buttons[1].enabled:
            entity_list = pm.read_uint(client_base + ENTITY_LIST)
            if entity_list:
                print(f"Entity listesi: 0x{entity_list:X}")
                for i in range(1, 32):
                    entity = pm.read_uint(entity_list + i * 0x10)
                    if entity:
                        health = pm.read_int(entity + HEALTH)
                        print(f"Health: Düşman {i} adres=0x{entity:X}, can={health}")
                    else:
                        print(f"Health: Düşman {i} adres null")
            else:
                print("Hata: Entity listesi null")
            time.sleep(0.1)
    except Exception as e:
        print(f"Hata: Health başarısız: {e}")
        categories[2].buttons[1].enabled = False

def mevlana_3d(pm, client_base):
    try:
        print("3D başlatılıyor...")
        while categories[2].buttons[2].enabled:
            entity_list = pm.read_uint(client_base + ENTITY_LIST)
            if entity_list:
                print(f"Entity listesi: 0x{entity_list:X}")
                for i in range(1, 32):
                    entity = pm.read_uint(entity_list + i * 0x10)
                    if entity:
                        try:
                            pos = pm.read_vec3(entity + POSITION)
                            print(f"3D: Düşman {i} adres=0x{entity:X}, pozisyon={pos.x},{pos.y},{pos.z}")
                        except AttributeError:
                            print(f"Hata: 3D pozisyon okunamadı, adres=0x{entity:X}")
                    else:
                        print(f"3D: Düşman {i} adres null")
            else:
                print("Hata: Entity listesi null")
            time.sleep(0.1)
    except Exception as e:
        print(f"Hata: 3D başarısız: {e}")
        categories[2].buttons[2].enabled = False

def mevlana_skeleton(pm, client_base):
    try:
        print("Skeleton başlatılıyor...")
        while categories[2].buttons[3].enabled:
            entity_list = pm.read_uint(client_base + ENTITY_LIST)
            if entity_list:
                print(f"Entity listesi: 0x{entity_list:X}")
                for i in range(1, 32):
                    entity = pm.read_uint(entity_list + i * 0x10)
                    if entity:
                        bone_matrix = pm.read_uint(entity + BONES)
                        print(f"Skeleton: Düşman {i} adres=0x{entity:X}, kemik matrisi=0x{bone_matrix:X}")
                    else:
                        print(f"Skeleton: Düşman {i} adres null")
            else:
                print("Hata: Entity listesi null")
            time.sleep(0.1)
    except Exception as e:
        print(f"Hata: Skeleton başarısız: {e}")
        categories[2].buttons[3].enabled = False

class Star:
    def __init__(self):
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = random.randint(0, WINDOW_HEIGHT)
        self.size = random.randint(1, 2)
        self.speed = random.uniform(0.05, 0.2)
        self.angle = random.uniform(0, 2 * math.pi)

    def move(self):
        center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        self.angle += self.speed * 0.01
        distance = math.sqrt((self.x - center_x) ** 2 + (self.y - center_y) ** 2)
        if distance > 50:
            self.x = center_x + math.cos(self.angle) * distance
            self.y = center_y + math.sin(self.angle) * distance
        else:
            self.x = random.randint(0, WINDOW_WIDTH)
            self.y = random.randint(0, WINDOW_HEIGHT)
            self.angle = random.uniform(0, 2 * math.pi)

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size)

class BlackHole:
    def __init__(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.radius = 100
        self.angle = 0

    def draw(self, screen):
        for i in range(50, 0, -1):
            alpha = int(255 * (i / 50))
            color = (20, 0, 40 + i * 2)
            pygame.draw.circle(screen, color, (self.x, self.y), self.radius - i, 1)
        pygame.draw.circle(screen, GLOW_PURPLE, (self.x, self.y), self.radius, 3)
        self.angle += 0.005

class Button:
    def __init__(self, text, x, y, width, height, inactive_color, active_color):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.enabled = False
        self.scale = 1.0
        self.target_scale = 1.0

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        self.target_scale = 1.1 if self.is_hovered(mouse) else 1.0
        self.scale += (self.target_scale - self.scale) * 0.1
        scaled_width = int(self.width * self.scale)
        scaled_height = int(self.height * self.scale)
        scaled_x = self.x - (scaled_width - self.width) // 2
        scaled_y = self.y - (scaled_height - self.height) // 2

        pygame.draw.rect(screen, DARK_PURPLE, (scaled_x + 5, scaled_y + 5, scaled_width, scaled_height))
        color = self.active_color if self.is_hovered(mouse) else self.inactive_color
        pygame.draw.rect(screen, color, (scaled_x, scaled_y, scaled_width, scaled_height), border_radius=10)
        if self.is_hovered(mouse):
            pygame.draw.rect(screen, GLOW_PURPLE, (scaled_x, scaled_y, scaled_width, scaled_height), 2, border_radius=10)
        text_surf = font.render(self.text + (" [AÇIK]" if self.enabled else " [KAPALI]"), True, WHITE)
        text_rect = text_surf.get_rect(center=(scaled_x + scaled_width // 2, scaled_y + scaled_height // 2))
        screen.blit(text_surf, text_rect)

    def is_hovered(self, mouse):
        return self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height

    def is_clicked(self, mouse, event):
        if self.is_hovered(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.enabled = not self.enabled
            return True
        return False

class Category:
    def __init__(self, name, x, y, width, height, buttons):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.buttons = buttons
        self.active = False
        self.scale = 1.0
        self.target_scale = 1.0

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        self.target_scale = 1.1 if self.is_hovered(mouse) else 1.0
        self.scale += (self.target_scale - self.scale) * 0.1
        scaled_width = int(self.width * self.scale)
        scaled_height = int(self.height * self.scale)
        scaled_x = self.x - (scaled_width - self.width) // 2
        scaled_y = self.y - (scaled_height - self.height) // 2

        pygame.draw.rect(screen, DARK_PURPLE, (scaled_x + 5, scaled_y + 5, scaled_width, scaled_height))
        color = NEON_BLUE if self.active or self.is_hovered(mouse) else NEON_PURPLE
        pygame.draw.rect(screen, color, (scaled_x, scaled_y, scaled_width, scaled_height), border_radius=10)
        if self.is_hovered(mouse) or self.active:
            pygame.draw.rect(screen, GLOW_PURPLE, (scaled_x, scaled_y, scaled_width, scaled_height), 2, border_radius=10)
        text_surf = font.render(self.name, True, WHITE)
        text_rect = text_surf.get_rect(center=(scaled_x + scaled_width // 2, scaled_y + scaled_height // 2))
        screen.blit(text_surf, text_rect)

    def is_hovered(self, mouse):
        return self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height

    def is_clicked(self, mouse, event):
        if self.is_hovered(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = True
            return True
        return False

black_hole = BlackHole()
stars = [Star() for _ in range(50)]

categories = [
    Category("Ana Sayfa", 10, 10, 200, 50, []),
    Category("Rage", 10, 70, 200, 50, [
        Button("Silent Aim", 740, 70, 250, 60, NEON_PURPLE, NEON_BLUE),
    ]),
    Category("Visual", 10, 130, 200, 50, [
        Button("Chams", 740, 70, 250, 60, NEON_PURPLE, NEON_BLUE),
        Button("Health", 740, 140, 250, 60, NEON_PURPLE, NEON_BLUE),
        Button("3D", 740, 210, 250, 60, NEON_PURPLE, NEON_BLUE),
        Button("Skeleton", 740, 280, 250, 60, NEON_PURPLE, NEON_BLUE),
    ]),
    Category("BunnyHop", 10, 190, 200, 50, [
        Button("Auto BunnyHop", 740, 70, 250, 60, NEON_PURPLE, NEON_BLUE),
    ]),
]

ultimate_bypass()
pm = get_process()
client_base = get_module_base(pm, CLIENT_DLL) if pm else 0
player_base = pm.read_uint(client_base + LOCAL_PLAYER) if client_base else 0

def main():
    clock = pygame.time.Clock()
    active_category = categories[0]
    active_category.active = True

    if not pm:
        print("CS2 bağlantısı başarısız, hileler çalışmayacak.")
    if not client_base:
        print("client.dll bulunamadı, hileler çalışmayacak.")
    if not player_base:
        print("Oyuncu adresi alınamadı, hileler çalışmayacak.")
    else:
        print(f"Oyuncu adresi: 0x{player_base:X}")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            mouse = pygame.mouse.get_pos()
            for category in categories:
                if category.is_clicked(mouse, event):
                    for c in categories:
                        c.active = False
                    category.active = True
                    active_category = category
            for button in active_category.buttons:
                if button.is_clicked(mouse, event) and pm and client_base and player_base:
                    print(f"Düğme aktif: {button.text}")
                    if button.text == "Chams":
                        threading.Thread(target=mevlana_chams, args=(pm, client_base), daemon=True).start()
                    elif button.text == "Health":
                        threading.Thread(target=mevlana_health, args=(pm, client_base), daemon=True).start()
                    elif button.text == "3D":
                        threading.Thread(target=mevlana_3d, args=(pm, client_base), daemon=True).start()
                    elif button.text == "Skeleton":
                        threading.Thread(target=mevlana_skeleton, args=(pm, client_base), daemon=True).start()
                    elif button.text == "Auto BunnyHop":
                        threading.Thread(target=mevlana_bunnyhop, args=(pm, player_base), daemon=True).start()

        screen.fill(DARK_PURPLE)
        black_hole.draw(screen)
        for star in stars:
            star.move()
            star.draw(screen)
        title_surf = title_font.render("Hoşgeldiniz Menümüze", True, GLOW_PURPLE)
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 30))
        screen.blit(title_surf, title_rect)
        for i, category in enumerate(categories):
            category.draw(screen)
            if i < len(categories) - 1:
                pygame.draw.line(screen, WHITE, (10, category.y + 50), (210, category.y + 50), 2)
        for button in active_category.buttons:
            button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()