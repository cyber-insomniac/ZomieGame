import pygame

class LevelUpMenu:
    def __init__(self):
        self.font = pygame.font.SysFont("Courier New", 11, bold=True)
        self.is_active = False
        
        self.btn1_rect = None
        self.btn2_rect = None

    def trigger(self):
        """Aktivuje menu při level upu"""
        self.is_active = True

    def update(self, events, player, window_scale):
        """Zpracovává volbu (klávesy 1/2 nebo kliknutí myší na tlačítka)"""
        if not self.is_active:
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    # Volba 1: Posun o zbraň dopředu / lepší úroveň melee
                    player.melee_damage = [d + 20 for d in player.melee_damage]
                    player.weapon = 0
                    self.is_active = False
                    
                elif event.key == pygame.K_e:
                    # Volba 2: Přepnutí na jiný typ zbraně (nebo posun u gunu)
                    player.gun_damage += 10
                    player.weapon = 1
                    self.is_active = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                scaled_mouse = (mx / window_scale, my / window_scale)

                if self.btn1_rect and self.btn1_rect.collidepoint(scaled_mouse):
                    player.melee_damage = [d + 20 for d in player.melee_damage]
                    player.weapon = 0
                    self.is_active = False
                elif self.btn2_rect and self.btn2_rect.collidepoint(scaled_mouse):
                    player.gun_damage += 10
                    player.weapon = 1
                    self.is_active = False

    def draw(self, surface, player):
        """Vykreslí menu s obrázky zbraní na tlačítkách"""
        if not self.is_active:
            return

        surface_width = surface.get_width()
        surface_height = surface.get_height()

        # Větší okno, aby se tam vedle textu vešly i obrázky zbraní
        menu_width = 280
        menu_height = 130
        menu_x = (surface_width - menu_width) // 2
        menu_y = (surface_height - menu_height) // 2

        # Pozadí menu
        pygame.draw.rect(surface, (80, 80, 80), (menu_x, menu_y, menu_width, menu_height))
        pygame.draw.rect(surface, (85, 74, 18), (menu_x, menu_y, menu_width, menu_height), 1)

        # Nadpis
        title_text = self.font.render("LEVEL UP!", False, (255, 255, 0))
        title_rect = title_text.get_rect(center=(surface_width // 2, menu_y + 15))
        surface.blit(title_text, title_rect)

        # --- TLAČÍTKO 1: Melee / Zbraň nablízko ---
        self.btn1_rect = pygame.Rect(menu_x + 10, menu_y + 35, menu_width - 20, 38)
        pygame.draw.rect(surface, (60, 60, 80), self.btn1_rect)
        pygame.draw.rect(surface, (255, 255, 255), self.btn1_rect, 1)
        
        # Text na tlačítku 1
        btn1_text = self.font.render("[USE_ABILITY] Melee Up", False, (255, 255, 255))
        surface.blit(btn1_text, (self.btn1_rect.x + 8, self.btn1_rect.y + 12))
        
        # Obrázek zbraně na tlačítku 1 (např. meč / MELEE_IMAGE z hráče)
        # Zmenšíme ho, aby se vešel na tlačítko (např. 24x24 pixelů)
        melee_icon = pygame.transform.scale(player.MELEE_IMAGE, (48, 15))
        surface.blit(melee_icon, (self.btn1_rect.right - 32, self.btn1_rect.y + 7))

        # --- TLAČÍTKO 2: Gun / Zbraň na dálku ---
        self.btn2_rect = pygame.Rect(menu_x + 10, menu_y + 80, menu_width - 20, 38)
        pygame.draw.rect(surface, (60, 60, 80), self.btn2_rect)
        pygame.draw.rect(surface, (255, 255, 255), self.btn2_rect, 1)
        
        # Text na tlačítku 2
        btn2_text = self.font.render("[PICK_UP] Gun Up", False, (255, 255, 255))
        surface.blit(btn2_text, (self.btn2_rect.x + 8, self.btn2_rect.y + 12))
        
        # Obrázek zbraně na tlačítku 2 (např. AK47 / GUN_IMAGE z hráče, nebo můžeš mít seznam zbraní)
        gun_icon = pygame.transform.scale(player.GUN_IMAGE, (48, 15)) # Uprav rozměr podle potřeby pušky
        surface.blit(gun_icon, (self.btn2_rect.right - 36, self.btn2_rect.y + 11))