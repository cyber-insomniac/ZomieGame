import pygame
import random
import math

from ability import ability

class AbilitySpawner:
    abilities = []
    abilityTypes = ["double_damage", "insta_kill", "granade", "bomb", "dynamite"]

    def __init__(self):
        self.spawn_timer = 0.0
        self.spawn_delay = 15.05251

    def spawn_ability(self):
        random_x = random.uniform(-2, 2)

        new_ability = ability(random_x, 0, 50, 50, "granade")
        AbilitySpawner.abilities.append(new_ability)

    def update(self, dt):

        self.spawn_timer += dt

        if self.spawn_timer >= self.spawn_delay:
            self.spawn_ability()
            self.spawn_timer = 0.0 

        for e in AbilitySpawner.abilities:
            e.update(dt)  

        AbilitySpawner.abilities = [a for a in AbilitySpawner.abilities if a.distance >= 2 and not a.pickedUp]

