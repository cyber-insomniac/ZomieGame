import math
import random

import pygame

from enemy import Enemy


class EnemySpawner:
  # Statická (třídní) proměnná – sdílená pro celou třídu
  enemies = []

  def __init__(self):
    self.spawn_timer = 0.0
    self.spawn_delay = 5.0

  def spawn_enemy(self):
    random_x = random.uniform(-2, 2)
    new_enemy = Enemy(random_x, 0, 50, 150, 100, 10)
    # Přidáváme do třídního seznamu
    EnemySpawner.enemies.append(new_enemy)

  def update(self, dt):
    self.spawn_timer += dt

    if self.spawn_timer >= self.spawn_delay:
      self.spawn_enemy()
      self.spawn_timer = 0.0

    # Procházíme třídní seznam
    for e in EnemySpawner.enemies:
      e.update(dt)

    # Filtrujeme třídní seznam
    EnemySpawner.enemies = [e for e in EnemySpawner.enemies if e.distance >= 2 and e.health > 0]

  def draw(self, surface):
    for e in EnemySpawner.enemies:
      e.draw(surface)