import pygame

from ability_spawner import AbilitySpawner
from enemy_spawner import EnemySpawner

class RenderingManager:

    def draw(self, surface):
        all_objects = EnemySpawner.enemies + AbilitySpawner.abilities

        sorted_objects = sorted(all_objects, key=lambda obj: obj.distance, reverse=True)

        for sprite in sorted_objects:
            sprite.draw(surface)

