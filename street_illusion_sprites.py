"""
Pseudo-3D pixel-art street illusion, built from your own sprites:
    street.png     - pre-drawn trapezoid, blitted statically (never reshaped)
    buildingL.png  - the single "nearest" left building (64x133, anchored
                      near its bottom-front/curb corner)
    buildingR.png  - mirror of the above for the right side
    streetline.png - one dash of the center line
    UI.png         - full-canvas HUD/frame overlay

All the perspective (position + scale) for buildings and dashes comes from
ONE projection function, tuned so it lines up with where street.png's
trapezoid already converges. Nothing is warped at runtime except uniform
nearest-neighbor scaling.

Buildings are spaced along the curb using each sprite's own world-space
footprint (derived from its pixel width), so consecutive copies sit flush
against each other instead of leaving gaps -- a continuous receding wall.
They keep growing and sliding toward the screen edges as they approach,
only recycling once they've genuinely moved off-frame (not at some fixed
"reference" depth), so nothing pops/vanishes early.

Controls: Left/Right or A/D to strafe, Up/Down or W/S to change speed, Esc to quit.
Requires: pip install pygame
Expects the 5 PNGs above in the same folder as this script (an "assets/" subfolder works too).
"""

import math
import os
import sys

import pygame

# ----------------------------------------------------------------------
# Config - derived from the geometry already baked into street.png
# ----------------------------------------------------------------------
INTERNAL_W, INTERNAL_H = 320, 180
WINDOW_SCALE = 3
WINDOW_W, WINDOW_H = INTERNAL_W * WINDOW_SCALE, INTERNAL_H * WINDOW_SCALE

HORIZON_Y = 32          # matches the apex row of street.png's trapezoid
VANISH_X = 160          # matches the horizontal center of that apex
FOCAL = 65.9            # solved so building anchors land on the curb corners
CAM_HEIGHT = 1.533
STREET_HALF_WIDTH = 2.2  # world units, curb distance from center

NEAR_Z_REF = 1.0   # depth the sprites were drawn for (scale = 1x here)
MIN_Z = 0.08        # recycle threshold - low, so things grow big & slide
                     # off-frame before disappearing, instead of popping
                     # away right at their native size
FAR_Z = 15.0         # spawn / far depth

FORWARD_SPEED = 3.0
STRAFE_SPEED = 1.6

SKY_COLOR = (25, 20, 40)

BUILDING_OVERLAP = 0.85   # <1 biases spacing to slightly overlap rather
                          # than risk a visible gap between buildings
DASH_SPACING = 2.0        # world units between successive centerline dashes

MAX_SPRITE_PX = INTERNAL_W * 4  # safety clamp so extreme close-ups don't
                                 # blow up into huge scaled surfaces


def find_asset(name):
    here = os.path.dirname(os.path.abspath(__file__))
    for candidate in (os.path.join(here, name), os.path.join(here, "assets", name)):
        if os.path.exists(candidate):
            return candidate
    raise FileNotFoundError(f"Could not find {name} next to this script (or in an assets/ folder).")


# ----------------------------------------------------------------------
# Projection
# ----------------------------------------------------------------------
def project(x_world, z, cam_x=0.0):
    z = max(z, 0.001)
    sx = VANISH_X + FOCAL * (x_world - cam_x) / z
    sy = HORIZON_Y + FOCAL * CAM_HEIGHT / z
    return sx, sy


def scale_mult(z):
    """1.0 at NEAR_Z_REF (sprite's native pixel size); grows past 1 as z
    keeps shrinking below that (object is closer than 'native' depth),
    shrinks toward 0 as z grows toward FAR_Z."""
    return NEAR_Z_REF / max(z, 0.001)


# ----------------------------------------------------------------------
# Sprite wrapper: crops the source image to its drawn content, remembers
# the anchor point (as a 0..1 fraction) that should sit on the projected
# world point, and derives the sprite's own world-space footprint width
# (used to space repeated copies without gaps).
# ----------------------------------------------------------------------
class AnchoredSprite:
    def __init__(self, path, anchor_frac):
        img = pygame.image.load(path).convert_alpha()
        bbox = img.get_bounding_rect()
        self.image = img.subsurface(bbox).copy()
        self.anchor_frac = anchor_frac  # (fx, fy) within the cropped image
        # world-space width this sprite occupies at its reference depth
        self.world_width = self.image.get_width() * NEAR_Z_REF / FOCAL

    def draw(self, surf, x_world, z, cam_x):
        sx, sy = project(x_world, z, cam_x)
        m = scale_mult(z)
        w = min(max(1, int(self.image.get_width() * m)), MAX_SPRITE_PX)
        h = min(max(1, int(self.image.get_height() * m)), MAX_SPRITE_PX)
        scaled = pygame.transform.scale(self.image, (w, h))  # nearest-neighbor look
        fx, fy = self.anchor_frac
        top_left = (int(sx - fx * w), int(sy - fy * h))
        surf.blit(scaled, top_left)


class Receding:
    """A row of identical sprites spaced along z on one side (or centered),
    recycling forward once they've moved off-frame."""

    def __init__(self, sprite, side_x, spacing, near=NEAR_Z_REF, far=FAR_Z, min_z=MIN_Z):
        self.sprite = sprite
        self.side_x = side_x  # world x of the curb/center line this row sits on
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
        for z in sorted(self.zs, reverse=True):  # far first
            self.sprite.draw(surf, self.side_x, z, cam_x)


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Pseudo-3D Street (your sprites)")
    internal = pygame.Surface((INTERNAL_W, INTERNAL_H))
    clock = pygame.time.Clock()

    street_img = pygame.image.load(find_asset("street.png")).convert_alpha()
    ui_img = pygame.image.load(find_asset("UI.png")).convert_alpha()

    # anchor fractions worked out from each sprite's bottom-front corner
    building_l = AnchoredSprite(find_asset("buildingL.png"), anchor_frac=(0.234, 1.0))
    building_r = AnchoredSprite(find_asset("buildingR.png"), anchor_frac=(0.75, 1.0))
    dash = AnchoredSprite(find_asset("streetline.png"), anchor_frac=(0.5, 1.0))

    left_row = Receding(building_l, -STREET_HALF_WIDTH, building_l.world_width * BUILDING_OVERLAP)
    right_row = Receding(building_r, STREET_HALF_WIDTH, building_r.world_width * BUILDING_OVERLAP)
    dash_row = Receding(dash, 0.0, DASH_SPACING)

    cam_x = 0.0
    speed = FORWARD_SPEED

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            cam_x -= STRAFE_SPEED * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            cam_x += STRAFE_SPEED * dt
        cam_x = max(-STREET_HALF_WIDTH * 0.8, min(STREET_HALF_WIDTH * 0.8, cam_x))
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            speed = min(speed + 3 * dt, 9)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            speed = max(speed - 3 * dt, 0.5)

        dz = speed * dt
        left_row.update(dz)
        right_row.update(dz)
        dash_row.update(dz)

        # ---- draw ----
        internal.fill(SKY_COLOR)
        internal.blit(street_img, (0, 0))
        dash_row.draw(internal, cam_x)
        left_row.draw(internal, cam_x)
        right_row.draw(internal, cam_x)
        internal.blit(ui_img, (0, 0))

        scaled = pygame.transform.scale(internal, (WINDOW_W, WINDOW_H))
        window.blit(scaled, (0, 0))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
