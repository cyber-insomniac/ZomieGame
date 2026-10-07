# events.py
import pygame

ENEMY_DAMAGE_EVENT = pygame.event.custom_type()
ABILITY_PICKEDUP_EVENT = pygame.event.custom_type()
ENEMY_DEATH_EVENT = pygame.event.custom_type()
GAMEOVER_EVENT = pygame.event.custom_type()