# program.py
import pygame
import sys

# Importing classes
from map_renderer import MapRenderer
from menu import Menu


WINDOW_SCALE = 3
INTERNAL_W, INTERNAL_H = 320, 180
WINDOW_W, WINDOW_H = INTERNAL_W * WINDOW_SCALE, INTERNAL_H * WINDOW_SCALE

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("Zombie Game")
        self.internal_surface = pygame.Surface((INTERNAL_W, INTERNAL_H))
        self.clock = pygame.time.Clock()
        self.running = True

        self.state = "MENU"  # Game state

        # Class initiation
        self.map = MapRenderer()
        self.menu = Menu()
        
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            
            mouse_clicked = False

            # Event Manager -----
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicked = True

            keys = pygame.key.get_pressed()
            
            mx, my = pygame.mouse.get_pos()
            scaled_mouse = (mx / WINDOW_SCALE, my / WINDOW_SCALE)

            # Draw and Update -----
            if self.state == "MENU":

                action = self.menu.update(scaled_mouse, mouse_clicked)
                
                if action == "START":
                    self.state = "GAME"
                elif action == "QUIT":
                    self.running = False
                
                self.menu.draw(self.internal_surface)

            elif self.state == "GAME":
                self.map.update(dt, keys)
                self.map.draw(self.internal_surface)


            # Window stuff idk
            scaled = pygame.transform.scale(self.internal_surface, (WINDOW_W, WINDOW_H))
            self.window.blit(scaled, (0, 0))
            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()