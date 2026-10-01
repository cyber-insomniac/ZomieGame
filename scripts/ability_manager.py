import pygame

from events import ABILITY_PICKEDUP_EVENT

from abilities.grenade import Grenade
from abilities.dynamite import Dynamite
from abilities.bomb import Bomb

class AbilityManager:

    def __init__(self):
        self.active_ability = ""
        self.ACTIVE_ABILITY_IMAGE = None

        self.rect = pygame.Rect(150,148,29,29)
        self.rect.center = (195,161)

        self.spawned_abilities = []
    
    def update(self,dt,events):
        for event in events:
            if event.type == ABILITY_PICKEDUP_EVENT:
                self.active_ability = event.name
                self.ACTIVE_ABILITY_IMAGE = event.image
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                print("kokot")
                self.use_active_ability()

        self.spawned_abilities = [g for g in self.spawned_abilities if g.active]
        for a in self.spawned_abilities:
            a.update(dt)

    def draw(self, surface):
        if self.ACTIVE_ABILITY_IMAGE != None:
            self.ACTIVE_ABILITY_IMAGE = pygame.transform.scale(self.ACTIVE_ABILITY_IMAGE, (self.rect.w, self.rect.h))
            surface.blit(self.ACTIVE_ABILITY_IMAGE, self.rect)
        elif self.active_ability != "":
            pygame.draw.rect(surface, (0,255,0), self.rect)

        for a in self.spawned_abilities:
            a.draw(surface)

    def use_active_ability(self):
        match self.active_ability:
            case "grenade":
                print("kokot2")
                self.use_grenade()
            case "bomb":
                self.use_bomb()
            case "dynamite":
                self.use_dynamite()
            case "double_damage":
                self.use_double_damage()
            case "inta_kill":
                self.use_insta_kill()


    def use_grenade(self):
        new_ability = Grenade(0)
        self.spawned_abilities.append(new_ability)
        self.active_ability = ""
        self.ACTIVE_ABILITY_IMAGE = None

    def use_bomb(self):
        new_ability = Bomb(0)
        self.spawned_abilities.append(new_ability)
        self.active_ability = ""
        self.ACTIVE_ABILITY_IMAGE = None

    def use_dynamite(self):
        new_ability = Dynamite(0)
        self.spawned_abilities.append(new_ability)
        self.active_ability = ""
        self.ACTIVE_ABILITY_IMAGE = None

    def use_double_damage(self):
        #new_ability = ()
        #self.spawned_abilities.append(new_ability)
        return None

    def use_insta_kill(self):
        #new_ability = Grenade()
        #self.spawned_abilities.append(new_ability)
        return None