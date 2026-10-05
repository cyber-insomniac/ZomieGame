import pygame
import json

from events import ENEMY_DAMAGE_EVENT, ABILITY_PICKEDUP_EVENT,ENEMY_DEATH_EVENT
from enemy_spawner import EnemySpawner
from ability_spawner import AbilitySpawner

from level_up_menu import LevelUpMenu

WINDOW_SCALE = 4
 
class Player_manager:

    damage_multiplier = 1.0

    def __init__(self):
        self.health = 10
        self.gun_damage = 10
        self.melee_damage = [20,40,60]
        self.rect = pygame.Rect(0,0,3,3)
        self.gun_rect = [10,10]
        self.melee_rect = [50,20]

        self.score = 0
        self.level = 1
        self.exp = 0
        self.next_level_exp = 100
        
        self.font = pygame.font.SysFont("Courier New", 12, bold=True)

        self.is_leveling_up = False

        with open("scripts/weapons/melees/sword.json", "r", encoding="utf-8") as json_file: # STARTING WEAPON
            self.weapon_data = json.load(json_file)
        
        self.SLASH_IMAGE = pygame.image.load("assets/slash.png").convert_alpha()
        self.CROSSHAIR_IMAGE = pygame.image.load("assets/crosshair.png").convert_alpha()

        self.MELEE_IMAGE = pygame.image.load("assets/sword.png").convert_alpha()
        self.GUN_IMAGE = pygame.image.load("assets/Ak47.png").convert_alpha()

        self.HEARTH_IMAGE = pygame.image.load("assets/Hearts.png")

        self.weapon = 0 # 0 = MELEE | 1 = GUN

        self.level_up_menu = LevelUpMenu()

    def update(self, dt, events):

        for event in events:
            if event.type == ENEMY_DAMAGE_EVENT:
                self.health -= event.amount
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_l: # Light hit
                        for enemy in EnemySpawner.enemies:
                            if pygame.Rect.colliderect(enemy.rect, self.rect):
                                if(self.weapon == 0):
                                    self.swing_melee(0, Player_manager.damage_multiplier, enemy)
                                else:
                                    self.shoot_gun(0, Player_manager.damage_multiplier, enemy)
                    case pygame.K_m: # Medium hit
                        for enemy in EnemySpawner.enemies:
                            if pygame.Rect.colliderect(enemy.rect, self.rect):
                                if(self.weapon == 0):
                                    self.swing_melee(1, Player_manager.damage_multiplier, enemy)
                                else:
                                    self.shoot_gun(2, Player_manager.damage_multiplier, enemy)
                    case pygame.K_h: # Hard hit
                        for enemy in EnemySpawner.enemies:
                            if pygame.Rect.colliderect(enemy.rect, self.rect):
                                if(self.weapon == 0):
                                    self.swing_melee(2, Player_manager.damage_multiplier, enemy)
                                else:
                                    self.shoot_gun(5, Player_manager.damage_multiplier, enemy)
                    case pygame.K_e:
                        for ability in AbilitySpawner.abilities:
                            if pygame.Rect.colliderect(ability.rect, self.rect):
                                if ability.distance < 5:
                                    ev = pygame.event.Event(ABILITY_PICKEDUP_EVENT, {"name": ability.ability_name, "image": ability.current_image})
                                    pygame.event.post(ev)
                                    ability.pickedUp = True
            elif event.type == ENEMY_DEATH_EVENT:
                self.add_score_and_exp(event.amount)

        if(self.weapon == 0):
            self.rect.width = self.melee_rect[0]
            self.rect.height = self.melee_rect[1]
        else:
            self.rect.width = self.gun_rect[0]
            self.rect.height = self.gun_rect[1]

        if self.level_up_menu.is_active:
            self.level_up_menu.update(events, self, WINDOW_SCALE)


        mx, my = pygame.mouse.get_pos()
        scaled_mouse = (mx / WINDOW_SCALE, my / WINDOW_SCALE)
        self.rect.center = scaled_mouse

    def draw(self, surface):
        # Target
        current_image = self.SLASH_IMAGE if self.weapon == 0 else self.CROSSHAIR_IMAGE
        scaled_image = pygame.transform.scale(current_image, (self.rect.width, self.rect.height))
        surface.blit(scaled_image, self.rect)

        # Weapon Indicator
        weapon_image = self.MELEE_IMAGE if self.weapon == 0 else self.GUN_IMAGE
        surface.blit(weapon_image, (216, 148))

        # Health Indicator
        for x in range(self.health):
            surface.blit(self.HEARTH_IMAGE, (x * 14 + 10, 148))

        # LEVEL bar
        surface_width = surface.get_width()

        bar_width = 120
        bar_height = 8
        bar_x = (surface_width - bar_width) // 2
        bar_y = 10

        ## BG color
        pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))

        ## 0.0-1.0
        progress = min(self.exp / self.next_level_exp, 1.0)
        filled_width = int(bar_width * progress)

        ## Fill color
        if filled_width > 0:
            pygame.draw.rect(surface, (0, 200, 100), (bar_x, bar_y, filled_width, bar_height))

        ## Border
        pygame.draw.rect(surface, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)

        ## Current Level
        level_text = self.font.render(f"Lvl. {self.level}", False, (255, 255, 255))
        surface.blit(level_text, (bar_x - 50, bar_y - 2))

        ## Score
        score_text = self.font.render(f"{self.score}", False, (255, 255, 255))
        score_x = bar_x + bar_width + 15
        score_y = bar_y + (bar_height // 2 + 1) - (score_text.get_height() // 2)
        surface.blit(score_text, (score_x, score_y))

        # Level Up
        self.level_up_menu.draw(surface, self)



    def swing_melee(self, amount, multiplier, enemy):
        if(enemy.distance < 8):
            enemy.health -= self.melee_damage[amount]
            if enemy.health <= 0:
                 ev = pygame.event.Event(ENEMY_DEATH_EVENT, {"amount": 100})
                 pygame.event.post(ev)

    def shoot_gun(self, amount, multiplier, enemy):
        for i in range(amount + 1):
            enemy.health -= self.gun_damage
            if enemy.health <= 0:
                 ev = pygame.event.Event(ENEMY_DEATH_EVENT, {"amount": 70})
                 pygame.event.post(ev)

    def add_score_and_exp(self, amount):
        self.score += amount
        self.exp += amount

        while self.exp >= self.next_level_exp:
            self.exp -= self.next_level_exp
            self.level += 1
            self.next_level_exp = int(self.next_level_exp * 1.5)

            # Spustíme nové menu
            self.level_up_menu.trigger()    





    ##### TODO #####
    # Magazine/Ammo
    # Abilities
    # Score
    # Menu
    # Art
    # Gameover state
    # !!!!BALANCING!!!!
 