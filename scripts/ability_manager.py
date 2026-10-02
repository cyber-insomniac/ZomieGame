import pygame

from events import ABILITY_PICKEDUP_EVENT

from abilities.throwable import Throwable

class AbilityManager:
    spawned_abilities = []

    def __init__(self):
        self.active_ability = ""
        self.ACTIVE_ABILITY_IMAGE = None

        self.rect = pygame.Rect(150,148,29,29)
        self.rect.center = (195,161)
    
    def update(self,dt,events):
        for event in events:
            if event.type == ABILITY_PICKEDUP_EVENT:
                self.active_ability = event.name
                self.ACTIVE_ABILITY_IMAGE = event.image
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                self.use_active_ability()

        AbilityManager.spawned_abilities = [g for g in AbilityManager.spawned_abilities if g.active]
        for a in AbilityManager.spawned_abilities:
            a.update(dt)

    def draw(self, surface):
        if self.ACTIVE_ABILITY_IMAGE != None:
            self.ACTIVE_ABILITY_IMAGE = pygame.transform.scale(self.ACTIVE_ABILITY_IMAGE, (self.rect.w, self.rect.h))
            surface.blit(self.ACTIVE_ABILITY_IMAGE, self.rect)
        elif self.active_ability != "":
            pygame.draw.rect(surface, (0,255,0), self.rect)

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
            case "inta_kill":
                self.use_insta_kill()


    def use_throwable(self, path):
        new_ability = Throwable(0, path)
        AbilityManager.spawned_abilities.append(new_ability)
        self.active_ability = ""
        self.ACTIVE_ABILITY_IMAGE = None

    def use_double_damage(self): #TODO
        self.active_ability = ""
        self.ACTIVE_ABILITY_IMAGE = None

    def use_insta_kill(self): #TODO
        self.active_ability = ""
        self.ACTIVE_ABILITY_IMAGE = None