# program.py
import pygame
import sys

# Importing classes
from map_renderer import MapRenderer


WINDOW_SCALE = 3
INTERNAL_W, INTERNAL_H = 320, 180
WINDOW_W, WINDOW_H = INTERNAL_W * WINDOW_SCALE, INTERNAL_H * WINDOW_SCALE

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("Moje super hra")
        self.internal_surface = pygame.Surface((INTERNAL_W, INTERNAL_H))
        self.clock = pygame.time.Clock()
        self.running = True

        # Class initiation
        self.map = MapRenderer()
        
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0

            # Event Manager --------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

            keys = pygame.key.get_pressed()

            # Update Function --------
            self.map.update(dt, keys)

            # FUTURE EXAMPLES vvvv
            # self.player.update(dt, keys)
            # self.enemies.update(dt)

            # Draw Function --------
            self.map.draw(self.internal_surface)

            # FUTURE EXAMPLES vvvv
            # self.player.draw(self.internal_surface)
            # self.enemies.draw(self.internal_surface)

            # Window stuff idk
            scaled = pygame.transform.scale(self.internal_surface, (WINDOW_W, WINDOW_H))
            self.window.blit(scaled, (0, 0))
            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()