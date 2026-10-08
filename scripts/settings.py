import pygame
import json
import os

class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        
        # Barvy tlačítek
        self.color_normal = (70, 70, 70)
        self.color_text = (255, 255, 255)
        
        self.is_hovered = False

    def update(self, mouse_pos, mouse_clicked):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if self.is_hovered and mouse_clicked:
            return True
        return False

    def draw(self, surface):
        color = self.color_normal
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, width=2, border_radius=5)

        text_surf = self.font.render(self.text, False, self.color_text)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

class Settings:
    # Obtížnost jako mapování čísla na název
    DIFFICULTIES = {
        1: "Easy",
        2: "Medium",
        4: "Hard",
        8: "Extreme"
    }

    # Interní rozlišení 320x180 vynásobené měřítkem
    SCALE_PRESETS = [
        (4, "4x (1280x720)"),
        (5, "5x (1600x900)"),
        (6, "6x (1920x1080)"),
        (7, "7x (2240x1260)")
    ]

    def __init__(self):
        self.font_title = pygame.font.SysFont("Arial", 26, bold=True)
        self.font_label = pygame.font.SysFont("Arial", 11, bold=True)
        self.font_btn = pygame.font.SysFont("Arial", 12)
        self.font_hint = pygame.font.SysFont("Arial", 10)

        self.title = self.font_title.render("Settings", False, (255, 200, 50))

        # Výchozí hodnoty: obtížnost 2 (Medium), měřítko 6
        self.difficulty = 2
        self.window_scale = 6

        self.load_settings()

        # 4 tlačítka obtížnosti (čísla 1, 2, 4, 8)
        self.diff_buttons = []
        btn_w, btn_h, gap = 48, 22, 4
        start_x = 58
        for i, (diff_num, name) in enumerate(self.DIFFICULTIES.items()):
            btn = Button(start_x + i * (btn_w + gap), 58, btn_w, btn_h, name, self.font_btn)
            self.diff_buttons.append((diff_num, btn))

        # Tlačítko rozlišení (širší, aby se vešel celý popisek rozlišení)
        scale_label = self.get_scale_label(self.window_scale)
        self.btn_scale = Button(80, 104, 160, 22, scale_label, self.font_btn)

        # Tlačítko zpět
        self.btn_back = Button(110, 148, 100, 22, "Back", self.font_btn)

    def get_scale_label(self, scale_val):
        for s, label in self.SCALE_PRESETS:
            if s == scale_val:
                return label
        return f"{scale_val}x"

    def get_filepath(self):
        here = os.path.dirname(os.path.abspath(__file__))
        folder = os.path.abspath(os.path.join(here, "..", "saves"))
        os.makedirs(folder, exist_ok=True)
        return os.path.join(folder, "settings.json")

    def load_settings(self):
        path = self.get_filepath()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.difficulty = int(data.get("difficulty", 2))
                    # Ošetření platných klíčů obtížnosti (1, 2, 4, 8)
                    if self.difficulty not in self.DIFFICULTIES:
                        self.difficulty = 2
                    self.window_scale = int(data.get("window_scale", 6))
            except Exception:
                pass

    def save_settings(self):
        path = self.get_filepath()
        data = {
            "difficulty": self.difficulty,
            "window_scale": self.window_scale
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def update(self, mouse_pos, mouse_clicked):
        # Výběr obtížnosti 1 až 8
        for diff_num, btn in self.diff_buttons:
            if btn.update(mouse_pos, mouse_clicked):
                self.difficulty = diff_num
                self.save_settings()

        # Cyklické přepínání rozlišení okna
        if self.btn_scale.update(mouse_pos, mouse_clicked):
            scale_values = [s[0] for s in self.SCALE_PRESETS]
            curr_idx = scale_values.index(self.window_scale) if self.window_scale in scale_values else 2
            next_idx = (curr_idx + 1) % len(scale_values)
            self.window_scale = scale_values[next_idx]
            self.btn_scale.text = self.get_scale_label(self.window_scale)
            self.save_settings()

        # Tlačítko zpět
        if self.btn_back.update(mouse_pos, mouse_clicked):
            return "BACK"

        return None

    def draw(self, surface):
        surface.fill((20, 20, 30))

        # Nadpis
        title_rect = self.title.get_rect(center=(160, 20))
        surface.blit(self.title, title_rect)

        # Popisek obtížnosti
        diff_label = self.font_label.render("DIFFICULTY", False, (200, 200, 200))
        surface.blit(diff_label, (58, 44))

        # Vykreslení tlačítek obtížnosti (aktivní zeleně)
        for diff_num, btn in self.diff_buttons:
            orig_color = btn.color_normal
            if diff_num == self.difficulty:
                btn.color_normal = (40, 140, 60)
            btn.draw(surface)
            btn.color_normal = orig_color

        # Popisek rozlišení
        scale_label = self.font_label.render("WINDOW RESOLUTION", False, (200, 200, 200))
        scale_label_rect = scale_label.get_rect(center=(160, 92))
        surface.blit(scale_label, scale_label_rect)
        self.btn_scale.draw(surface)

        # Nápověda k restartu hry
        hint = self.font_hint.render("*Requires game restart", False, (140, 140, 150))
        surface.blit(hint, (160 - hint.get_width() // 2, 131))

        # Tlačítko Back
        self.btn_back.draw(surface)