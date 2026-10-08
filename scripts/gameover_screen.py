import pygame
import os


class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        
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


class GameOverScreen:
    def __init__(self):
        self.font_title = pygame.font.SysFont("Arial", 24, bold=True)
        self.font_score = pygame.font.SysFont("Arial", 14)
        self.font_input = pygame.font.SysFont("Arial", 14)
        self.font_btn = pygame.font.SysFont("Arial", 14)
        
        self.title = self.font_title.render("GAME OVER", False, (250, 50, 50))
        
        self.finalscore = 0
        self.player_name = ""
        self.input_active = False
        self.is_saved = False 
        
        # Textové pole na jméno
        self.input_rect = pygame.Rect(60, 75, 200, 26)
        
        # Tlačítka pod sebou (bez restartu, srovnaná výška)
        self.btn_save = Button(60, 110, 200, 24, "Save Score", self.font_btn)
        self.btn_menu = Button(60, 140, 200, 24, "Main Menu", self.font_btn)

    def update(self, mouse_pos, mouse_clicked, events, final_score, window_scale=1):
        self.finalscore = final_score
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Opraveno: Přepočítáme event.pos pomocí window_scale, aby odpovídalo herním souřadnicím
                scaled_event_pos = (event.pos[0] / window_scale, event.pos[1] / window_scale)
                self.input_active = self.input_rect.collidepoint(scaled_event_pos)
                
            elif event.type == pygame.KEYDOWN and self.input_active and not self.is_saved:
                if event.key == pygame.K_RETURN:
                    self.save_score()
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                else:
                    if len(self.player_name) < 12 and event.unicode.isprintable() and event.unicode != " ":
                        self.player_name += event.unicode

        if not self.is_saved and self.btn_save.update(mouse_pos, mouse_clicked):
            self.save_score()
            
        if self.btn_menu.update(mouse_pos, mouse_clicked):
            self.is_saved = False
            self.player_name = ""
            return "MAIN_MENU"
            
        return None

    def save_score(self):
        if self.is_saved:
            return
            
        name = self.player_name.strip()
        if not name:
            name = "Anonym"
            
        here = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.abspath(os.path.join(here, "..", "saves"))
        os.makedirs(folder_path, exist_ok=True)
        filepath = os.path.join(folder_path, "highscores.txt")
        
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(f"\n{name} {self.finalscore}")
            
        self.is_saved = True

    def draw(self, surface):
        surface.fill((20, 20, 30))
        
        title_rect = self.title.get_rect(center=(surface.get_width() // 2, 25))
        surface.blit(self.title, title_rect)

        score_surf = self.font_score.render(f"Final Score: {self.finalscore}", False, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(surface.get_width() // 2, 53))
        surface.blit(score_surf, score_rect)

        # Vykreslení textového pole
        border_color = (150, 150, 200) if self.input_active else (80, 80, 100)
        pygame.draw.rect(surface, (30, 30, 40), self.input_rect, border_radius=4)
        pygame.draw.rect(surface, border_color, self.input_rect, width=2, border_radius=4)
        
        if self.is_saved:
            display_text = "SAVED!"
            text_color = (100, 255, 100)
        elif self.player_name == "" and not self.input_active:
            display_text = "Enter name..."
            text_color = (120, 120, 120)
        else:
            display_text = self.player_name + ("|" if self.input_active else "")
            text_color = (255, 255, 255)
            
        txt_surface = self.font_input.render(display_text, False, text_color)
        surface.blit(txt_surface, (self.input_rect.x + 8, self.input_rect.y + 5))

        self.btn_save.draw(surface)
        self.btn_menu.draw(surface)