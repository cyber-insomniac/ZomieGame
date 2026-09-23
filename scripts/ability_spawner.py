import pygame
import random
import math

from ability import ability

class AbilitySpawner:

    abilityTypes = ["double_damage", "insta_kill", "granade"]

    def __init__(self):
        self.abilities = []

        self.spawn_timer = 0.0
        self.spawn_delay = 7.15

    def spawn_ability(self):
        random_x = random.uniform(-2, 2)

        new_ability = ability(random_x, 0, 50, 50, "granade")
        self.abilities.append(new_ability)

    def update(self, dt):

        self.spawn_timer += dt

        if self.spawn_timer >= self.spawn_delay:
            self.spawn_ability()
            self.spawn_timer = 0.0 

        for e in self.abilities:
            e.update(dt)  

        self.abilities = [a for a in self.abilities if a.distance >= 2]

    def draw(self, surface):
        for a in self.abilities:
            a.draw(surface)
