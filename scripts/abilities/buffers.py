import pygame
import json
import os
from player_manager import Player_manager

class Bufferes:
    def __init__(self):
        self.font = pygame.font.SysFont("Courier New", 10, bold=True)
        self.instakill_timer = 0.0
        self.doubledamage_timer = 0.0

        # Načtení dat z JSON souborů (s fallback výchozími hodnotami)
        self.instakill_duration, self.instakill_mult = self.load_buff_data("instakill.json", 5.0, 99999)
        self.doubledamage_duration, self.doubledamage_mult = self.load_buff_data("doubledamage.json", 30.0, 2.0)

    def load_buff_data(self, filename, default_dur, default_mult):
        here = os.path.dirname(os.path.abspath(__file__))
        # Zkontroluje cesty k JSONům (např. scripts/weapons/ nebo abilities/)
        potential_paths = [
            os.path.join(here, filename),
            os.path.join(here, "abilities", filename),
            os.path.join(here, "..", "scripts", "abilities", filename)
        ]
        for path in potential_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        return data.get("duration", default_dur), data.get("multiplier", default_mult)
                except Exception:
                    pass
        return default_dur, default_mult

    def reset(self):
        self.instakill_timer = 0.0
        self.doubledamage_timer = 0.0
        Player_manager.damage_multiplier = 1.0

    def trigger_instakill(self):
        # Resetuje časovač na celou dobu trvání
        self.instakill_timer = self.instakill_duration
        self.update_multiplier()

    def trigger_doubledamage(self):
        # Resetuje časovač na celou dobu trvání
        self.doubledamage_timer = self.doubledamage_duration
        self.update_multiplier()

    def update_multiplier(self):
        if self.instakill_timer > 0:
            Player_manager.damage_multiplier = self.instakill_mult
        elif self.doubledamage_timer > 0:
            Player_manager.damage_multiplier = self.doubledamage_mult
        else:
            Player_manager.damage_multiplier = 1.0

    def update(self, dt):
        if self.instakill_timer > 0:
            self.instakill_timer -= dt
            if self.instakill_timer <= 0:
                self.instakill_timer = 0.0
                self.update_multiplier()

        if self.doubledamage_timer > 0:
            self.doubledamage_timer -= dt
            if self.doubledamage_timer <= 0:
                self.doubledamage_timer = 0.0
                self.update_multiplier()

    def draw(self, surface):
        y_offset = 100
        margin_right = 10

        if self.instakill_timer > 0:
            text = f"INSTA KILL!!!! ({int(self.instakill_timer + 1)})"
            surf = self.font.render(text, False, (255, 30, 30))
            rect = surf.get_rect(topright=(surface.get_width() - margin_right, y_offset))
            surface.blit(surf, rect)
            y_offset += 14

        if self.doubledamage_timer > 0:
            text = f"2x DAMAGE ({int(self.doubledamage_timer + 1)})"
            surf = self.font.render(text, False, (218, 165, 32))
            rect = surf.get_rect(topright=(surface.get_width() - margin_right, y_offset))
            surface.blit(surf, rect)