# map_renderer.py
import math
import os
import pygame

INTERNAL_W, INTERNAL_H = 320, 180
HORIZON_Y = 32
VANISH_X = 160
FOCAL = 65.9
CAM_HEIGHT = 1.533
STREET_HALF_WIDTH = 2.2
NEAR_Z_REF = 1.0
MIN_Z = 0.08
FAR_Z = 15.0
FORWARD_SPEED = 0.7
SKY_COLOR = (25, 20, 40)
BUILDING_OVERLAP = 0.85
DASH_SPACING = 2.0
MAX_SPRITE_PX = INTERNAL_W * 4


def find_asset(name):
    here = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.abspath(os.path.join(here, "..", "assets", name))
    if os.path.exists(candidate): return candidate
    raise FileNotFoundError(f"Could not find {name} at {candidate}")

def project(x_world, z, cam_x=0.0):
    z = max(z, 0.001)
    sx = VANISH_X + FOCAL * (x_world - cam_x) / z
    sy = HORIZON_Y + FOCAL * CAM_HEIGHT / z
    return sx, sy

def scale_mult(z):
    return NEAR_Z_REF / max(z, 0.001)


class AnchoredSprite:
    def __init__(self, path, anchor_frac):
        img = pygame.image.load(path).convert_alpha()
        bbox = img.get_bounding_rect()
        self.image = img.subsurface(bbox).copy()
        self.anchor_frac = anchor_frac
        self.world_width = self.image.get_width() * NEAR_Z_REF / FOCAL

    def draw(self, surf, x_world, z, cam_x):
        sx, sy = project(x_world, z, cam_x)
        m = scale_mult(z)
        w = min(max(1, int(self.image.get_width() * m)), MAX_SPRITE_PX)
        h = min(max(1, int(self.image.get_height() * m)), MAX_SPRITE_PX)
        scaled = pygame.transform.scale(self.image, (w, h))
        fx, fy = self.anchor_frac
        top_left = (int(sx - fx * w), int(sy - fy * h))
        surf.blit(scaled, top_left)

class Receding:
    def __init__(self, sprite, side_x, spacing, near=NEAR_Z_REF, far=FAR_Z, min_z=MIN_Z):
        self.sprite = sprite
        self.side_x = side_x
        self.spacing = spacing
        self.min_z = min_z
        self.far = far
        span = far - min_z
        count = max(1, math.ceil(span / spacing) + 1)
        self.zs = [near + i * spacing for i in range(count)]

    def update(self, dz):
        span = self.far - self.min_z
        for i in range(len(self.zs)):
            self.zs[i] -= dz
            if self.zs[i] < self.min_z:
                self.zs[i] += span

    def draw(self, surf, cam_x):
        for z in sorted(self.zs, reverse=True):
            self.sprite.draw(surf, self.side_x, z, cam_x)


# Constuctor
# Constructor
class MapRenderer:
    def __init__(self):
        self.street_img = pygame.image.load(find_asset("street2.png")).convert_alpha()
        self.ui_img = pygame.image.load(find_asset("UI2.png")).convert_alpha()
        self.backgroundImg = pygame.image.load(find_asset("Backgroundblue_with_MOON2.png"))

        building_l = AnchoredSprite(find_asset("buildingL2.png"), anchor_frac=(0.234, 1.0))
        building_r = AnchoredSprite(find_asset("buildingR2.png"), anchor_frac=(0.75, 1.0))
        dash = AnchoredSprite(find_asset("streetline2.png"), anchor_frac=(0.5, 1.0))
        

        self.left_row = Receding(building_l, -STREET_HALF_WIDTH, building_l.world_width * BUILDING_OVERLAP)
        self.right_row = Receding(building_r, STREET_HALF_WIDTH, building_r.world_width * BUILDING_OVERLAP)
        self.dash_row = Receding(dash, 0.0, DASH_SPACING)

        # We keep cam_x initialized to 0.0 so we can still pass it to the draw 
        # functions and enemy spawner without causing errors, but it will never change.
        self.cam_x = 0.0
        self.speed = FORWARD_SPEED

    def update(self, dt, keys):
        dz = self.speed * dt
        self.left_row.update(dz)
        self.right_row.update(dz)
        self.dash_row.update(dz)

    def draw(self, surface):
        surface.blit(self.backgroundImg, (0,0))
        surface.blit(self.street_img, (0, 0))
        
        # We pass self.cam_x (which is always 0.0) so the perspective calculations still work
        self.dash_row.draw(surface, self.cam_x)
        self.left_row.draw(surface, self.cam_x)
        self.right_row.draw(surface, self.cam_x)
        surface.blit(self.ui_img, (0, 0))