import math
import random

import pygame

from enemy import Enemy


class EnemySpawner:
  enemies = []

  def __init__(self, difficulty):
    self.reset(difficulty)

  def reset(self, difficulty):
    self.spawn_timer = 4.0
    self.spawn_delay = 5.0
    self.enemy_health = 100
    self.difficulty = difficulty
    EnemySpawner.enemies.clear()

  def spawn_enemy(self):
    random_x = random.uniform(-2, 2)
    new_enemy = Enemy(random_x, 0, 38 * 3, 60 * 3, self.enemy_health, 1)
    EnemySpawner.enemies.append(new_enemy)

    self.enemy_health += self.difficulty
    self.spawn_delay = max(1.0, self.spawn_delay - (0.025 * self.difficulty))

  def update(self, dt):
    self.spawn_timer += dt

    if self.spawn_timer >= self.spawn_delay:
      self.spawn_enemy()
      self.spawn_timer = 0.0

    for e in EnemySpawner.enemies:
      e.update(dt)

    EnemySpawner.enemies = [e for e in EnemySpawner.enemies if e.distance >= 2 and e.health > 0]
