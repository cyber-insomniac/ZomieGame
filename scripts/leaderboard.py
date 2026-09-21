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


class Leaderboard:
    def __init__(self):
        self.font_title = pygame.font.SysFont("Arial", 30, bold=True)
        self.font_btn = pygame.font.SysFont("Arial", 16)
        self.font_score = pygame.font.SysFont("Arial", 14) 
        
        self.title = self.font_title.render("Leaderboard", True, (255, 200, 50))
        
        self.btn_back = Button(110, 150, 100, 25, "Back", self.font_btn)

        self.scores = self.load_highscores(limit=5)
        
    def load_highscores(self, limit):
        here = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.abspath(os.path.join(here, "..", "saves", "highscores.txt"))

        all_scores = []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        name = parts[0]
                        try:
                            score = int(parts[1])
                            all_scores.append((name, score))
                        except ValueError:
                            pass
        except FileNotFoundError:
            pass
            
        # Sorting score
        all_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Top [limit]
        return all_scores[:limit]

    def update(self, mouse_pos, mouse_clicked):     
        if self.btn_back.update(mouse_pos, mouse_clicked):
            return "BACK"
            
        return None

    def draw(self, surface):
        surface.fill((20, 20, 30))
        
        title_rect = self.title.get_rect(center=(160, 25))
        surface.blit(self.title, title_rect)

        start_y = 50
        line_height = 18
        
        if not self.scores:
            box_height = 33
        else:
            box_height = max(line_height * len(self.scores) + 10, 20)

        box_rect = pygame.Rect(60, start_y - 5, 200, box_height)
        pygame.draw.rect(surface, (30, 30, 40), box_rect)
        pygame.draw.rect(surface, (100, 100, 100), box_rect, width=1)


        if not self.scores:
            text_surf = self.font_score.render("Empty..", True, (150, 150, 150))
            text_rect = text_surf.get_rect(center=(160, start_y + 10))
            surface.blit(text_surf, text_rect)
        else:
            for i, (name, score) in enumerate(self.scores):
                y_pos = start_y + (i * line_height)
                
                rank_str = f"{i + 1}. {name}"
                score_str = str(score)
                
                rank_surf = self.font_score.render(rank_str, True, (255, 255, 255))
                score_surf = self.font_score.render(score_str, True, (255, 200, 50))
                
                surface.blit(rank_surf, (65, y_pos))

                surface.blit(score_surf, (255 - score_surf.get_width(), y_pos))

        self.btn_back.draw(surface)