import pygame
import sys
import json
import os

def get_initial_settings():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.abspath(os.path.join(here, "..", "saves", "settings.json"))
    scale = 6
    diff = 2  # Výchozí hodnota 2 (Medium)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                scale = int(data.get("window_scale", 6))
                diff = int(data.get("difficulty", 2))
                if diff not in range(1, 5):
                    diff = 2
        except Exception:
            pass
    return scale, diff

WINDOW_SCALE, INITIAL_DIFFICULTY = get_initial_settings()
INTERNAL_W, INTERNAL_H = 320, 180
WINDOW_W, WINDOW_H = INTERNAL_W * WINDOW_SCALE, INTERNAL_H * WINDOW_SCALE

# Importing classes
from map_renderer import MapRenderer
from menu import Menu
from leaderboard import Leaderboard
from settings import Settings
from tutorial import Tutorial
from enemy_spawner import EnemySpawner
from ability_spawner import AbilitySpawner
from player_manager import Player_manager
from rendering_manager import RenderingManager
from ability_manager import AbilityManager
from gameover_screen import GameOverScreen

from events import GAMEOVER_EVENT


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("Zombie Game")
        self.internal_surface = pygame.Surface((INTERNAL_W, INTERNAL_H))
        self.clock = pygame.time.Clock()
        self.running = True

        self.state = "MENU"
        self.final_score = 0
        self.difficulty = INITIAL_DIFFICULTY

        # Class initiation
        self.map = MapRenderer()
        self.menu = Menu()
        self.leaderboard = Leaderboard()
        self.settings = Settings()
        self.tutorial = Tutorial()
        self.enemyspawner = EnemySpawner(self.difficulty)
        self.abilityspawner = AbilitySpawner()
        self.player_manager = Player_manager(self.difficulty)
        self.rendering_manager = RenderingManager()
        self.abilitymanager = AbilityManager()
        self.gameover_screen = GameOverScreen()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            mouse_clicked = False

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.state != "GAMEOVER":
                        self.state = "MENU"
                elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                    mouse_clicked = True
                elif event.type == GAMEOVER_EVENT:
                    self.final_score = event.score
                    self.state = "GAMEOVER"

            keys = pygame.key.get_pressed()
            mx, my = pygame.mouse.get_pos()
            scaled_mouse = (mx / WINDOW_SCALE, my / WINDOW_SCALE)

            if self.state == "MENU":
                pygame.mouse.set_visible(True)
                action = self.menu.update(scaled_mouse, mouse_clicked)

                if action == "START":
                    self.state = "GAME"
                elif action == "LEADERBOARD":
                    self.state = "LEADERBOARD"
                elif action == "SETTINGS":
                    self.state = "SETTINGS"
                elif action == "TUTORIAL":
                    self.state = "TUTORIAL"
                elif action == "QUIT":
                    self.running = False

                self.menu.draw(self.internal_surface)

            elif self.state == "LEADERBOARD":
                pygame.mouse.set_visible(True)
                action = self.leaderboard.update(scaled_mouse, mouse_clicked)
                if action == "BACK":
                    self.state = "MENU"
                self.leaderboard.draw(self.internal_surface)

            elif self.state == "SETTINGS":
                pygame.mouse.set_visible(True)
                action = self.settings.update(scaled_mouse, mouse_clicked)
                if action == "BACK":
                    self.difficulty = self.settings.difficulty
                    self.state = "MENU"
                self.settings.draw(self.internal_surface)

            elif self.state == "TUTORIAL":
                pygame.mouse.set_visible(True)
                action = self.tutorial.update(scaled_mouse, mouse_clicked)
                if action == "BACK":
                    self.state = "MENU"
                self.tutorial.draw(self.internal_surface)

            elif self.state == "GAME":
                pygame.mouse.set_visible(False)
                self.map.draw(self.internal_surface)
                self.abilitymanager.draw(self.internal_surface)
                self.rendering_manager.draw(self.internal_surface)
                self.player_manager.update(dt, events)
                self.player_manager.draw(self.internal_surface)

                if not self.player_manager.level_up_menu.is_active:
                    self.enemyspawner.update(dt)
                    self.abilityspawner.update(dt)
                    self.abilitymanager.update(dt, events)
                    self.map.update(dt, keys)

            elif self.state == "GAMEOVER":
                pygame.mouse.set_visible(True)
                action = self.gameover_screen.update(scaled_mouse, mouse_clicked, events, self.final_score, WINDOW_SCALE)
                if action == "MAIN_MENU":
                    self.reset()
                    self.state = "MENU"
                self.gameover_screen.draw(self.internal_surface)

            scaled = pygame.transform.scale(self.internal_surface, (WINDOW_W, WINDOW_H))
            self.window.blit(scaled, (0, 0))
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def reset(self):
        self.abilitymanager.reset()
        self.abilityspawner.reset()
        self.enemyspawner.reset(self.difficulty)
        self.player_manager.reset(self.difficulty)
        self.leaderboard.reload()
        self.final_score = 0


if __name__ == "__main__":
    game = Game()
    game.run()