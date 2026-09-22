import pygame
import math

class ability:
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

    angle = 0

    def __init__(self, x, y, width, height, health, damage):

        self.rect = pygame.Rect(x, y, width, height)
        self.y = y
        self.x = x
        self.height = height
        self.width = width

    def update(self, dt):   
        # Move ability closer over time
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

    def draw(self, surface):
        color = (0, 255, 0)
        pygame.draw.rect(surface, color, self.rect)


