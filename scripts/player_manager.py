import pygame
import json

from events import ENEMY_DAMAGE_EVENT, ABILITY_PICKEDUP_EVENT
from enemy_spawner import EnemySpawner
from ability_spawner import AbilitySpawner

from weapons.guns.gun import Gun
from weapons.melees.melee import Melee

WINDOW_SCALE = 4
 
class Player_manager:
    def __init__(self):
        self.health = 10
        self.gun_damage = 10
        self.melee_damage = [20,40,60]
        self.rect = pygame.Rect(0,0,3,3)
        self.gun_rect = [10,10]
        self.melee_rect = [50,20]

        with open("scripts/weapons/melees/sword.json", "r", encoding="utf-8") as json_file: # STARTING WEAPON
            self.weapon_data = json.load(json_file)
        
        self.SLASH_IMAGE = pygame.image.load("assets/slash.png").convert_alpha()
        self.CROSSHAIR_IMAGE = pygame.image.load("assets/crosshair.png").convert_alpha()

        self.MELEE_IMAGE = pygame.image.load("assets/sword.png").convert_alpha()
        self.GUN_IMAGE = pygame.image.load("assets/Ak47.png").convert_alpha()

        self.HEARTH_IMAGE = pygame.image.load("assets/Hearts.png")

        self.weapon = 0 # 0 = MELEE | 1 = GUN

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
                                    self.swing_melee(0,enemy)
                                else:
                                    self.shoot_gun(0, enemy)
                    case pygame.K_m: # Medium hit
                        for enemy in EnemySpawner.enemies:
                            if pygame.Rect.colliderect(enemy.rect, self.rect):
                                if(self.weapon == 0):
                                    self.swing_melee(1,enemy)
                                else:
                                    self.shoot_gun(2, enemy)
                    case pygame.K_h: # Hard hit
                        for enemy in EnemySpawner.enemies:
                            if pygame.Rect.colliderect(enemy.rect, self.rect):
                                if(self.weapon == 0):
                                    self.swing_melee(2,enemy)
                                else:
                                    self.shoot_gun(5, enemy)
                    case pygame.K_e:
                        for ability in AbilitySpawner.abilities:
                            if pygame.Rect.colliderect(ability.rect, self.rect):
                                if ability.distance < 5:
                                    ev = pygame.event.Event(ABILITY_PICKEDUP_EVENT, {"name": ability.ability_name, "image": ability.current_image})
                                    pygame.event.post(ev)
                                    ability.pickedUp = True

        if(self.weapon == 0):
            self.rect.width = self.melee_rect[0]
            self.rect.height = self.melee_rect[1]
        else:
            self.rect.width = self.gun_rect[0]
            self.rect.height = self.gun_rect[1]

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
        



    def swing_melee(self, amount, enemy):
        if(enemy.distance < 8):
            enemy.health -= self.melee_damage[amount]

    def shoot_gun(self, amount, enemy):
        for i in range(amount + 1):
            enemy.health -= self.gun_damage


    ##### TODO #####
    # Magazine/Ammo
    # Abilities
    # Score
    # Menu
    # Art
    # Gameover state
    # !!!!BALANCING!!!!
 