# menu.py
import pygame
import os

class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        
        # Button colors
        self.color_normal = (70, 70, 70)
        self.color_hover = (100, 100, 100)
        self.color_text = (255, 255, 255)
        
        self.is_hovered = False

    def update(self, mouse_pos, mouse_clicked):
        # Mouse detection for hover
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Mouse click detection
        if self.is_hovered and mouse_clicked:
            return True
        return False

    def draw(self, surface):
        # Button Drawing
        color = self.color_hover if self.is_hovered else self.color_normal
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        
        # Button border Drawing
        pygame.draw.rect(surface, (200, 200, 200), self.rect, width=2, border_radius=5)

        # Text centering
        text_surf = self.font.render(self.text, True, self.color_text)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


class Menu:
    def __init__(self):
        self.font_title = pygame.font.SysFont("Arial", 30, bold=True)
        self.font_btn = pygame.font.SysFont("Arial", 16)
        
        self.title = self.font_title.render("Zombie Game", True, (255, 200, 50))

        # Button Iniciation
        self.btn_start = Button(110, 65, 100, 30, "Play", self.font_btn)
        self.btn_leaderboard = Button(110, 100, 100, 30, "Leaderboard", self.font_btn)
        self.btn_quit = Button(110, 135, 100, 30, "Quit", self.font_btn)

    def update(self, mouse_pos, mouse_clicked):
        # Button functions
        if self.btn_start.update(mouse_pos, mouse_clicked):
            return "START"
        if self.btn_leaderboard.update(mouse_pos, mouse_clicked):
            return "LEADERBOARD"
        if self.btn_quit.update(mouse_pos, mouse_clicked):
            return "QUIT"
        
        return None

    def draw(self, surface):
        surface.fill((20, 20, 30))
        
        title_rect = self.title.get_rect(center=(160, 40))
        surface.blit(self.title, title_rect)

        self.btn_start.draw(surface)
        self.btn_leaderboard.draw(surface)
        self.btn_quit.draw(surface)