import pygame

from events import ABILITY_PICKEDUP_EVENT

class AbilityManager:

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
            elif event.type == pygame.KEYDOWN:
                 self.use_active_ability()

    def draw(self, surface):
        if self.ACTIVE_ABILITY_IMAGE != None:
            self.ACTIVE_ABILITY_IMAGE = pygame.transform.scale(self.ACTIVE_ABILITY_IMAGE, (self.rect.w, self.rect.h))
            surface.blit(self.ACTIVE_ABILITY_IMAGE, self.rect)
        elif self.active_ability != "":
            pygame.draw.rect(surface, (0,255,0), self.rect)

    def use_active_ability():
        return None