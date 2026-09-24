import pygame

from events import ENEMY_DAMAGE_EVENT
from enemy_spawner import EnemySpawner
from ability_spawner import AbilitySpawner

WINDOW_SCALE = 3
 
class Player_manager:
    def __init__(self):
        self.health = 100
        self.gun_damage = 10
        self.sword_damage = [20,40,60]
        self.rect = pygame.Rect(0,0,3,3)
        self.gun_rect = [10,10]
        self.sword_rect = [50,20]
        self.font = pygame.font.SysFont("Arial", 16)

        self.weapon = 1 # 0 = SWORD | 1 = GUN

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
                                    self.swing_sword(0,enemy)
                                else:
                                    self.shoot_gun(0, enemy)
                    case pygame.K_m: # Medium hit
                        for enemy in EnemySpawner.enemies:
                            if pygame.Rect.colliderect(enemy.rect, self.rect):
                                if(self.weapon == 0):
                                    self.swing_sword(1,enemy)
                                else:
                                    self.shoot_gun(1, enemy)
                    case pygame.K_h: # Hard hit
                        for enemy in EnemySpawner.enemies:
                            if pygame.Rect.colliderect(enemy.rect, self.rect):
                                if(self.weapon == 0):
                                    self.swing_sword(1,enemy)
                                else:
                                    self.shoot_gun(1, enemy)
                    case pygame.K_a:
                        for ability in AbilitySpawner.abilities:
                            if pygame.Rect.colliderect(ability.rect, self.rect):
                                if ability.distance < 5:
                                    ability.pickedUp = True

        if(self.weapon == 0):
            self.rect.width = self.sword_rect[0]
            self.rect.height = self.sword_rect[1]
        else:
            self.rect.width = self.gun_rect[0]
            self.rect.height = self.gun_rect[1]

        mx, my = pygame.mouse.get_pos()
        scaled_mouse = (mx / WINDOW_SCALE, my / WINDOW_SCALE)
        self.rect.center = scaled_mouse

    def draw(self, surface):
        # Target
        color = (255, 0, 0)
        pygame.draw.rect(surface, color, self.rect)

        # Weapon Indicator
        weapon_text = self.font.render("Sword" if self.weapon == 0 else "Gun", False, (0, 0, 0))
        surface.blit(weapon_text, (10,150))

        # Health Indicator
        health_text = self.font.render(f"{self.health}/100", False, (0, 0, 0))
        surface.blit(health_text, (100,200))

    def swing_sword(self, amount, enemy):
        if(enemy.distance < 8):
            enemy.health -= self.sword_damage[amount]

    def shoot_gun(self, amount, enemy):
        for i in range(amount + 1):
            enemy.health -= self.gun_damage


        
 