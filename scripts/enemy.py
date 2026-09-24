import pygame
import math

from events import ENEMY_DAMAGE_EVENT
 
 
class Enemy:
    speed = 1.5
 
    x = 0
    y = 0
    distance = 18
 
    width = 0
    height = 0
 
    scaled_height = 0
    scaled_width = 0
    scaled_y = 0
    scaled_x = 0
 
    VANISH_X = 160
    VANISH_Y = 32
    FOCAL = 65.9
    CAM_HEIGHT = 1.533
    NEAR_Z_REF = 1.0
 
    scale = 0
 
 
    def __init__(self, x, y, width, height, health, damage):
 
        self.rect = pygame.Rect(x, y, width, height)
        self.y = y
        self.x = x
        self.height = height
        self.width = width
        self.damage = damage
        self.health = health
        self.ZOMBIE_IMAGE_FULL = pygame.image.load("assets/Zombie.png").convert_alpha()
        self.ZOMBIE_IMAGE_HALF = pygame.image.load("assets/Zombie_took_hits.png").convert_alpha()
 
    def update(self, dt):  
        # Move enemy closer over time
            self.distance -= self.speed * dt
            z = max(self.distance, 0.001)
 
            # Calculate scale multiplier based on depth (Z)
            scale = self.NEAR_Z_REF / z
            scaled_width = self.width * scale
            scaled_height = self.height * scale
 
            # Project 3D world coordinates to 2D screen pixels (matching map_renderer)
            cam_x = 0.0
            scaled_x = self.VANISH_X + self.FOCAL * (self.x - cam_x) / z
            scaled_y = self.VANISH_Y + self.FOCAL * self.CAM_HEIGHT / z
 
            self.rect.update(self.x,self.y,scaled_width,scaled_height)
            self.rect.center = (scaled_x, scaled_y)
 
            self.deal_damage()
 
    def draw(self, surface):
        # Choose sprite based on health
        current_image = self.ZOMBIE_IMAGE_FULL if self.health > 50 else self.ZOMBIE_IMAGE_HALF

        # Scale the image to match the updated rectangle size
        scaled_image = pygame.transform.scale(current_image, (self.rect.width, self.rect.height))

        # Render scaled image to the surface
        surface.blit(scaled_image, self.rect)
 
    def deal_damage(self):
        if self.distance <= 2:
            ev = pygame.event.Event(ENEMY_DAMAGE_EVENT, {'amount': self.damage})
            pygame.event.post(ev)
 
 