import pygame
from menu import Button

class Tutorial:
    def __init__(self):
        self.font_title = pygame.font.SysFont("Arial", 28, bold=True)
        self.font_btn = pygame.font.SysFont("Arial", 16)
        self.font_text = pygame.font.SysFont("Arial", 11)

        self.title = self.font_title.render("Tutorial", True, (255, 200, 50))
        self.btn_back = Button(110, 148, 100, 22, "Back", self.font_btn)

        self.guide_lines = [
            "L Key  - Light Attack (Low damage / Fast)",
            "M Key  - Medium Attack (Moderate damage)",
            "H Key  - Heavy Attack (High damage / Burst)",
            "R Key  - Reload current firearm",
            "E Key  - Pick up spawned abilities",
            "Level Up freezes game to choose an upgrade."
        ]

    def update(self, mouse_pos, mouse_clicked):
        if self.btn_back.update(mouse_pos, mouse_clicked):
            return "BACK"
        return None

    def draw(self, surface):
        surface.fill((20, 20, 30))

        title_rect = self.title.get_rect(center=(160, 22))
        surface.blit(self.title, title_rect)

        # Rámeček
        box_rect = pygame.Rect(35, 42, 250, 100)
        pygame.draw.rect(surface, (30, 30, 40), box_rect)
        pygame.draw.rect(surface, (100, 100, 100), box_rect, width=1)

        # Řádky textu
        for i, line in enumerate(self.guide_lines):
            line_surf = self.font_text.render(line, True, (220, 220, 230))
            surface.blit(line_surf, (42, 48 + i * 15))

        self.btn_back.draw(surface)