import pygame
import os
from menu import Button

class Tutorial:
    def __init__(self):
        self.font_btn = pygame.font.SysFont("Arial", 12)

        # Načtení a škálování všech vrstev na rozměr 320x180
        here = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(here, "..", "assets")

        def load_layer(filename):
            path = os.path.join(assets_dir, filename)
            # Pokud by soubor ještě neexistoval (např. tutorial_2.png), vytvoří se prázdná průhledná plocha
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
            else:
                img = pygame.Surface((320, 180), pygame.SRCALPHA)
            return pygame.transform.scale(img, (320, 180))

        self.bg_book = load_layer("old_book.png")
        self.pages = [
            load_layer("tutorial_1.png"),
            load_layer("tutorial_1.png")
        ]

        self.current_page = 0  # 0 = První strana, 1 = Druhá strana

        # Tlačítka vpravo dole (rozvrženo vedle sebe)
        # Celková plocha: šířka 320, výška 180
        self.btn_page = Button(195, 154, 48, 18, "Next >", self.font_btn)
        self.btn_back = Button(245, 154, 48, 18, "Back", self.font_btn)

    def update(self, mouse_pos, mouse_clicked):
        # Přepínání stránek (cyklicky mezi stranou 1 a 2)
        if self.btn_page.update(mouse_pos, mouse_clicked):
            self.current_page = (self.current_page + 1) % len(self.pages)
            self.btn_page.text = "< Prev" if self.current_page == 1 else "Next >"

        # Tlačítko zpět do menu
        if self.btn_back.update(mouse_pos, mouse_clicked):
            self.current_page = 0
            self.btn_page.text = "Next >"
            return "BACK"

        return None

    def draw(self, surface):
        # 1. Podklad knihy (320x180)
        surface.blit(self.bg_book, (0, 0))

        # 2. Aktuální vrstva tutorialu (průhledné PNG nad knihou)
        surface.blit(self.pages[self.current_page], (0, 0))

        # 3. Tlačítka vpravo dole
        self.btn_page.draw(surface)
        self.btn_back.draw(surface)