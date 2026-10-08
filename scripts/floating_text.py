import pygame

class FloatingText:
    def __init__(self, x, y, text, color, lifetime=0.6, speed=40):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.lifetime = lifetime       # Celková doba trvání v sekundách
        self.timer = lifetime
        self.speed = speed             # Rychlost stoupání nahoru v px/s

    def update(self, dt):
        self.timer -= dt
        self.y -= self.speed * dt      # Pohyb textu nahoru

    def is_alive(self):
        return self.timer > 0

    def draw(self, surface, font):
        text_surf = font.render(self.text, False, self.color)
        rect = text_surf.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(text_surf, rect)