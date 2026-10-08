import pygame
import json

from events import ENEMY_DAMAGE_EVENT, ABILITY_PICKEDUP_EVENT,ENEMY_DEATH_EVENT, GAMEOVER_EVENT
from enemy_spawner import EnemySpawner
from ability_spawner import AbilitySpawner
from floating_text import FloatingText

from level_up_menu import LevelUpMenu

WINDOW_SCALE = 6
 
class Player_manager:

    damage_multiplier = 1.0

    def __init__(self, difficulty):
        self.font = pygame.font.SysFont("Courier New", 12, bold=True)
        self.gun_font = pygame.font.SysFont("Courier New", 12, bold=False)

        with open("scripts/weapons/weapon_sequence.json", "r", encoding="utf-8") as json_file:
            self.weapon_sequence = json.load(json_file)
        
        self.SLASH_IMAGE = pygame.image.load("assets/slash.png").convert_alpha()
        self.CROSSHAIR_IMAGE = pygame.image.load("assets/crosshair.png").convert_alpha()

        self.MELEE_IMAGES = []
        self.GUN_IMAGES = []
        for id in self.weapon_sequence["melees"]:
            image = pygame.image.load(id["image"]).convert_alpha()
            self.MELEE_IMAGES.append(image)

        for id in self.weapon_sequence["guns"]:
            image = pygame.image.load(id["image"]).convert_alpha()
            self.GUN_IMAGES.append(image)

        self.HEARTH_IMAGE = pygame.image.load("assets/Hearts.png")

        self.floating_texts = []

        self.reset(difficulty)
        self.level_up_menu = LevelUpMenu()


    def reset(self, difficulty):
        self.health = 10
        self.gun_damage = 10
        self.melee_damage = [20,40,60]
        self.rect = pygame.Rect(0,0,3,3)
        self.gun_rect = [11,11]
        self.melee_rect = [50,20]

        self.score = 0
        self.level = 0
        self.exp = 0
        self.next_level_exp = 300

        self.difficulty = difficulty

        self.is_leveling_up = False

        self.melee_level = 0
        self.gun_level = -1

        self.is_reloading = False

        first_gun = self.weapon_sequence["guns"][0]
        self.burst = first_gun["burst"]
        self.max_mag_ammo = first_gun["mag_size"]
        self.mag_ammo = first_gun["mag_size"]
        self.total_ammo = first_gun["total_ammo"]
        self.reload_duration = first_gun["reload_time"]
        self.gun_damage = first_gun["damage"]
        self.GUN_IMAGE = self.GUN_IMAGES[0]

        fisrt_melee = self.weapon_sequence["melees"][0]
        self.melee_damage = fisrt_melee["damage"]
        self.MELEE_IMAGE = self.MELEE_IMAGES[0]

        Player_manager.damage_multiplier = 0

        self.floating_texts.clear()

        self.weapon = 0 # 0 = MELEE | 1 = GUN

    def update(self, dt, events):

        for event in events:
            if event.type == ENEMY_DAMAGE_EVENT:
                self.health -= event.amount
                if self.health <= 0:
                    ev = pygame.event.Event(GAMEOVER_EVENT, {"score": self.score})
                    pygame.event.post(ev)

            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_l:  # Light
                        self.floating_texts.append(
                            FloatingText(self.rect.centerx, self.rect.top - 5, "Light", (200, 200, 200), lifetime=0.5, speed=30)
                        )
                        if self.weapon == 0:
                            for enemy in EnemySpawner.enemies:
                                if pygame.Rect.colliderect(enemy.rect, self.rect):
                                    self.swing_melee(0, Player_manager.damage_multiplier, enemy)
                                    break
                        else:
                            hit_enemy = next((e for e in EnemySpawner.enemies if pygame.Rect.colliderect(e.rect, self.rect)), None)
                            self.shoot_gun(self.burst[0], Player_manager.damage_multiplier, hit_enemy)

                    case pygame.K_m:  # Medium
                        self.floating_texts.append(
                            FloatingText(self.rect.centerx, self.rect.top - 5, "Medium!", (255, 215, 0), lifetime=0.6, speed=45)
                        )
                        if self.weapon == 0:
                            for enemy in EnemySpawner.enemies:
                                if pygame.Rect.colliderect(enemy.rect, self.rect):
                                    self.swing_melee(1, Player_manager.damage_multiplier, enemy)
                                    break
                        else:
                            hit_enemy = next((e for e in EnemySpawner.enemies if pygame.Rect.colliderect(e.rect, self.rect)), None)
                            self.shoot_gun(self.burst[1], Player_manager.damage_multiplier, hit_enemy)

                    case pygame.K_h:  # Hard
                        self.floating_texts.append(
                            FloatingText(self.rect.centerx, self.rect.top - 5, "HARD!!!", (230, 0, 0), lifetime=0.8, speed=60)
                        )
                        if self.weapon == 0:
                            for enemy in EnemySpawner.enemies:
                                if pygame.Rect.colliderect(enemy.rect, self.rect):
                                    self.swing_melee(2, Player_manager.damage_multiplier, enemy)
                                    break
                        else:
                            hit_enemy = next((e for e in EnemySpawner.enemies if pygame.Rect.colliderect(e.rect, self.rect)), None)
                            self.shoot_gun(self.burst[2], Player_manager.damage_multiplier, hit_enemy)

                    case pygame.K_e:
                        for ability in AbilitySpawner.abilities:
                            if pygame.Rect.colliderect(ability.rect, self.rect):
                                if ability.distance < 5:
                                    ev = pygame.event.Event(ABILITY_PICKEDUP_EVENT, {"name": ability.ability_name, "image": ability.current_image})
                                    pygame.event.post(ev)
                                    ability.pickedUp = True

            elif event.type == ENEMY_DEATH_EVENT:
                self.add_score_and_exp(event.amount)

        if(self.weapon == 0):
            self.rect.width = self.melee_rect[0]
            self.rect.height = self.melee_rect[1]
        else:
            self.rect.width = self.gun_rect[0]
            self.rect.height = self.gun_rect[1]

        if self.is_reloading: # Reloading
            self.reload_timer -= dt 
            if self.reload_timer <= 0:
                if self.max_mag_ammo <= self.total_ammo:
                    self.mag_ammo = self.max_mag_ammo
                    self.total_ammo -= self.max_mag_ammo
                else:
                    self.mag_ammo = self.total_ammo
                    self.total_ammo = 0

                self.is_reloading = False

        if self.level_up_menu.is_active:
            self.level_up_menu.update(events, self, WINDOW_SCALE)


        mx, my = pygame.mouse.get_pos()
        scaled_mouse = (mx / WINDOW_SCALE, my / WINDOW_SCALE)
        self.rect.center = scaled_mouse

        if self.mag_ammo <= 0:
            self.start_reload()

        for ft in self.floating_texts:
            ft.update(dt)
        self.floating_texts = [ft for ft in self.floating_texts if ft.is_alive()]

    def draw(self, surface):
        # Target
        current_image = self.SLASH_IMAGE if self.weapon == 0 else self.CROSSHAIR_IMAGE
        scaled_image = pygame.transform.scale(current_image, (self.rect.width, self.rect.height))
        surface.blit(scaled_image, self.rect)

        # Weapon Indicator
        weapon_image = self.MELEE_IMAGE if self.weapon == 0 else self.GUN_IMAGE
        surface.blit(weapon_image, (216, 148))

        # Health Indicator
        for x in range(self.health):
            surface.blit(self.HEARTH_IMAGE, (x * 14 + 10, 148))

        # Gun Indicator
        if self.weapon == 1:
            total_ammo_text = self.gun_font.render(f"{self.total_ammo}", False, (255, 255, 255))
            mag_ammo_text = self.gun_font.render(f"{self.mag_ammo}", False, (255, 255, 255))
            timer_text = self.gun_font.render(f"{self.reload_duration}", False, (255, 255, 255))
            
        else:
            total_ammo_text = self.gun_font.render(f"-", False, (255, 255, 255))
            mag_ammo_text = self.gun_font.render(f"-", False, (255, 255, 255))
            timer_text = self.gun_font.render(f"-", False, (255, 255, 255))

        surface.blit(total_ammo_text, (30,164))
        surface.blit(mag_ammo_text, (95,164))
        surface.blit(timer_text, (150,164))

        # Hit indicator
        for ft in self.floating_texts:
            ft.draw(surface, self.font)

        # LEVEL bar
        surface_width = surface.get_width()

        bar_width = 120
        bar_height = 8
        bar_x = (surface_width - bar_width) // 2
        bar_y = 10

        ## BG color
        pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))

        ## 0.0-1.0
        progress = min(self.exp / self.next_level_exp, 1.0)
        filled_width = int(bar_width * progress)

        ## Fill color
        if filled_width > 0:
            pygame.draw.rect(surface, (0, 200, 10), (bar_x, bar_y, filled_width, bar_height))

        ## Border
        pygame.draw.rect(surface, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)

        ## Current Level
        level_text = self.font.render(f"Lvl. {self.level}", False, (255, 255, 255))
        surface.blit(level_text, (bar_x - 50, bar_y - 2))

        ## Score
        score_text = self.font.render(f"{self.score}", False, (255, 255, 255))
        score_x = bar_x + bar_width + 15
        score_y = bar_y + (bar_height // 2 + 1) - (score_text.get_height() // 2)
        surface.blit(score_text, (score_x, score_y))

        # Level Up
        self.level_up_menu.draw(surface, self)



    def swing_melee(self, amount, multiplier, enemy):
        if(enemy.distance < 8):
            enemy.health -= (self.melee_damage[amount] * self.damage_multiplier)
            if enemy.health <= 0:
                 ev = pygame.event.Event(ENEMY_DEATH_EVENT, {"amount": 100})
                 pygame.event.post(ev)

    def shoot_gun(self, amount, multiplier, enemy):
        if self.is_reloading:
            return

        for i in range(amount):
            if self.mag_ammo > 0:
                self.mag_ammo -= 1
                if enemy != None:
                    enemy.health -= (self.gun_damage * self.damage_multiplier)
            else:
                self.start_reload()
                break
            if enemy != None:
                if enemy.health <= 0:
                    ev = pygame.event.Event(ENEMY_DEATH_EVENT, {"amount": 70})
                    pygame.event.post(ev)

    def start_reload(self):
        if not self.is_reloading and self.total_ammo != 0:
            self.is_reloading = True
            self.reload_timer = self.reload_duration


    def add_score_and_exp(self, amount):
        self.score += amount
        self.exp += amount

        while self.exp >= self.next_level_exp:
            self.exp -= self.next_level_exp
            self.level += 1
            self.next_level_exp = int(self.next_level_exp * (1 + 0.25  * self.difficulty))

            # Spustíme nové menu
            self.level_up_menu.trigger()   

    def upgrade_melee(self):
            self.weapon = 0 

            max_melee_index = len(self.weapon_sequence["melees"]) - 1   

            if self.melee_level < max_melee_index:
                self.melee_level += 1

                self.MELEE_IMAGE = self.MELEE_IMAGES[self.melee_level]
                self.melee_damage = self.weapon_sequence["melees"][self.melee_level]["damage"]
            else:
                self.melee_damage = [dmg + 50 for dmg in self.melee_damage]

        
    def upgrade_gun(self):
        self.weapon = 1
        max_gun_index = len(self.weapon_sequence["guns"]) - 1

        if self.gun_level < max_gun_index:
            self.gun_level += 1
            self.GUN_IMAGE = self.GUN_IMAGES[self.gun_level]
            
            gun_data = self.weapon_sequence["guns"][self.gun_level]

            self.gun_damage = gun_data["damage"]
            self.reload_duration = gun_data["reload_time"]

            self.total_ammo = gun_data["total_ammo"]
            self.max_mag_ammo = gun_data["mag_size"]
            self.mag_ammo = gun_data["mag_size"]

            self.burst = gun_data["burst"]

        else:
            self.gun_damage += 30
            self.total_ammo += 1000
            self.mag_ammo = self.max_mag_ammo



    ##### TODO #####
    # Magazine/Ammo
    # Abilities
    # Score
    # Menu
    # Art
    # Gameover state
    # !!!!BALANCING!!!!
 