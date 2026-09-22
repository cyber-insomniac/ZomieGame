import pygame
import random
import math

from enemy import Enemy

class EnemySpawner:
    def __init__(self):
        self.enemies = []

        self.spawn_timer = 0.0
        self.spawn_delay = 5.0

    def spawn_enemy(self):
        random_x = random.uniform(-2, 2)

        new_enemy = Enemy(random_x, 0, 50, 150, 10, 10)
        self.enemies.append(new_enemy)

    def update(self, dt):

        self.spawn_timer += dt

        if self.spawn_timer >= self.spawn_delay:
            self.spawn_enemy()
            self.spawn_timer = 0.0 

        for e in self.enemies:
            e.update(dt)  

        self.enemies = [e for e in self.enemies if e.distance >= 2]

    def draw(self, surface):
        for e in self.enemies:
            e.draw(surface)
