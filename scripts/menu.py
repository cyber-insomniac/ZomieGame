import pygame
import os

class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        
        # Barvy tlačítek
        self.color_normal = (70, 70, 70)
        self.color_hover = (100, 100, 100)
        self.color_text = (255, 255, 255)
        
        self.is_hovered = False

    def update(self, mouse_pos, mouse_clicked):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if self.is_hovered and mouse_clicked:
            return True
        return False

    def draw(self, surface):
        color = self.color_hover if self.is_hovered else self.color_normal
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, width=2, border_radius=5)

        text_surf = self.font.render(self.text, False, self.color_text)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


class ImageButton:
    def __init__(self, x, y, size, image_path, icon_padding=2):
        self.rect = pygame.Rect(x, y, size, size)
        
        # Načtení a zmenšení ikony tak, aby měla okolo sebe padding
        icon_size = max(1, size - (icon_padding * 2))
        raw_img = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(raw_img, (icon_size, icon_size))
        self.image_rect = self.image.get_rect(center=self.rect.center)
        
        # Barvy rámečku/podkladu (stejné jako u běžného Buttonu)
        self.color_normal = (70, 70, 70)
        self.color_hover = (100, 100, 100)
        self.border_color = (200, 200, 200)
        
        self.is_hovered = False

    def update(self, mouse_pos, mouse_clicked):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if self.is_hovered and mouse_clicked:
            return True
        return False

    def draw(self, surface):
        # Podkladové tlačítko
        color = self.color_hover if self.is_hovered else self.color_normal
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, self.border_color, self.rect, width=2, border_radius=5)
        
        # Vykreslení centrované ikonky
        surface.blit(self.image, self.image_rect)


class Menu:
    def __init__(self):
        self.font_title = pygame.font.SysFont("Arial", 30, bold=True)
        self.font_btn = pygame.font.SysFont("Arial", 16)
        
        self.title = self.font_title.render("Zombie Game", False, (255, 200, 50))

        # Hlavní akční tlačítka
        self.btn_start = Button(110, 65, 100, 30, "Play", self.font_btn)
        self.btn_leaderboard = Button(110, 102, 100, 30, "Leaderboard", self.font_btn)

        # 3 čtvercová tlačítka vedle sebe (šířka 30px, mezera 5px)
        # Celková šířka trojice je 100px (30 + 5 + 30 + 5 + 30), takže sedí přesně na šířku horních tlačítek (x: 110 až 210)
        btn_y = 140
        btn_size = 32
        self.btn_settings = ImageButton(110, btn_y, btn_size, "assets/settings_icon.png")
        self.btn_tutorial = ImageButton(145, btn_y, btn_size, "assets/help_icon.png")
        self.btn_quit = ImageButton(180, btn_y, btn_size, "assets/quit.png")

    def update(self, mouse_pos, mouse_clicked):
        if self.btn_start.update(mouse_pos, mouse_clicked):
            return "START"
        if self.btn_leaderboard.update(mouse_pos, mouse_clicked):
            return "LEADERBOARD"
            
        # Akce pro čtvercové ikony
        if self.btn_settings.update(mouse_pos, mouse_clicked):
            return "SETTINGS"
        if self.btn_tutorial.update(mouse_pos, mouse_clicked):
            return "TUTORIAL"
        if self.btn_quit.update(mouse_pos, mouse_clicked):
            return "QUIT"
        
        return None

    def draw(self, surface):
        surface.fill((20, 20, 30))
        
        title_rect = self.title.get_rect(center=(160, 40))
        surface.blit(self.title, title_rect)

        self.btn_start.draw(surface)
        self.btn_leaderboard.draw(surface)
        
        # Vykreslení čtvercových ikon
        self.btn_settings.draw(surface)
        self.btn_tutorial.draw(surface)
        self.btn_quit.draw(surface)