import pygame
import math
import json
import os

from enemy_spawner import EnemySpawner

class Throwable:

    VANISH_X = 160
    VANISH_Y = 32
    FOCAL = 65.9
    CAM_HEIGHT = 1.533
    NEAR_Z_REF = 1.0
    
    def __init__(self, x_start, json_path):

        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        file_path = os.path.join(current_dir, json_path)
        
        with open(file_path, "r", encoding="utf-8") as json_file:
            self.data = json.load(json_file)

        self.x = x_start
        self.y = 1.5          
        self.distance = 0.5

        # Throw
        self.speed_z = self.data["speed_z"]
        self.speed_y = self.data["speed_y"]
        self.gravity = 15.0 

        self.width = 15
        self.height = 15
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.exploded = False
        self.active = True

        self.image = pygame.image.load(self.data["image_path"]).convert_alpha()

    def update(self, dt):
        if not self.active:
            return

        if not self.exploded:
            self.distance += self.speed_z * dt       # Forward move
            self.speed_y -= self.gravity * dt        # Gravity
            self.y += self.speed_y * dt              # Height

            # Ground hit
            if self.y <= 0:
                self.y = 0
                self.explode()

        # Fake perspective
        z = max(self.distance, 0.001)
        scale = (self.NEAR_Z_REF / z) * 2.0
        
        scaled_width = self.width * scale
        scaled_height = self.height * scale

        cam_x = 0.0
        scaled_x = self.VANISH_X + self.FOCAL * (self.x - cam_x) / z
        scaled_y = self.VANISH_Y + self.FOCAL * (self.CAM_HEIGHT - self.y) / z

        self.rect.width = max(1, int(scaled_width))
        self.rect.height = max(1, int(scaled_height))
        self.rect.midbottom = (int(scaled_x), int(scaled_y))

    def explode(self):
        self.exploded = True
        self.active = False

        # Explosion config
        explosion_data = {
            "z": self.distance, 
            "radius": self.data["radius"],
            "damage": self.data["damage"]
        }
        self.explosion(explosion_data)

    def explosion(self, ed):
        ex_z = ed["z"]
        radius = ed["radius"]
        damage = ed["damage"]
        
        for enemy in EnemySpawner.enemies:
            dist_to_explosion = abs(enemy.distance - ex_z)
            
            if dist_to_explosion <= radius:
                enemy.health -= damage

    def draw(self, surface):
        if self.active:
            scaled_image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
            surface.blit(scaled_image, self.rect)