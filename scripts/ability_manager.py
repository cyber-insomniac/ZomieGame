import pygame
from events import ABILITY_PICKEDUP_EVENT
from abilities.throwable import Throwable
from abilities.buffers import Bufferes

class AbilityManager:
    spawned_abilities = []

    def __init__(self):
        self.rect = pygame.Rect(150, 148, 29, 29)
        self.rect.center = (195, 161)
        self.buffers = Bufferes()
        self.reset()

    def reset(self):
        self.active_ability = ""
        self.ACTIVE_ABILITY_IMAGE = None
        self.buffers.reset()
        AbilityManager.spawned_abilities.clear()

    def update(self, dt, events):
        for event in events:
            if event.type == ABILITY_PICKEDUP_EVENT:
                self.active_ability = event.name
                self.ACTIVE_ABILITY_IMAGE = event.image
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                self.use_active_ability()

        # Update odpočtů běžících buffů
        self.buffers.update(dt)

        AbilityManager.spawned_abilities = [g for g in AbilityManager.spawned_abilities if g.active]
        for a in AbilityManager.spawned_abilities:
            a.update(dt)

    def draw(self, surface):
        # Vykreslení ikony v inventáři
        if self.ACTIVE_ABILITY_IMAGE is not None:
            scaled_img = pygame.transform.scale(self.ACTIVE_ABILITY_IMAGE, (self.rect.w, self.rect.h))
            surface.blit(scaled_img, self.rect)
        elif self.active_ability != "":
            pygame.draw.rect(surface, (0, 255, 0), self.rect)

        # Vykreslení textů aktivních buffů v rohu obrazovky
        self.buffers.draw(surface)

    def use_active_ability(self):
        match self.active_ability:
            case "grenade":
                self.use_throwable("grenade.json")
            case "bomb":
                self.use_throwable("bomb.json")
            case "dynamite":
                self.use_throwable("dynamite.json")
            case "double_damage":
                self.use_double_damage()
            case "insta_kill":
                self.use_insta_kill()

    def use_throwable(self, path):
        new_ability = Throwable(0, path)
        AbilityManager.spawned_abilities.append(new_ability)
        self.active_ability = ""
        self.ACTIVE_ABILITY_IMAGE = None

    def use_double_damage(self):
        self.buffers.trigger_doubledamage()
        self.active_ability = ""
        self.ACTIVE_ABILITY_IMAGE = None

    def use_insta_kill(self):
        self.buffers.trigger_instakill()
        self.active_ability = ""
        self.ACTIVE_ABILITY_IMAGE = None