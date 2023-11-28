from typing import Any
import pygame

import random

from pygame.locals import (
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

rand = -200

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 212, 92))
        self.rect = self.surf.get_rect(
            center = (960, 540)
        )
    
    def update(self, pressed_keys):
        if pressed_keys[K_SPACE]:
            self.rect.move_ip(0, -2.5)
        else:
            self.rect.move_ip(0, 1)

        if self.rect.left < 0:
            self.rect.left = 0   
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class top_pipe(pygame.sprite.Sprite):
    def __init__(self):
        super(top_pipe, self).__init__()
        self.surf = pygame.Surface((200, 1080))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center = (2000, rand)
        )
        self.speed = 2

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class bottom_pipe(pygame.sprite.Sprite):
    def __init__(self):
        new = rand + 1400
        super(bottom_pipe, self).__init__()
        self.surf = pygame.Surface((200, 1080))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center = (2000, new)
        )
        self.speed = 2

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1500)

player = Player()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_top_pipe = top_pipe()
            new_bottom_pipe = bottom_pipe()
            enemies.add(new_top_pipe)
            enemies.add(new_bottom_pipe)
            all_sprites.add(new_top_pipe)
            all_sprites.add(new_bottom_pipe)
            rand = random.randint(-400, 100) 

    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)

    enemies.update()

    screen.fill((115, 215, 255))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    screen.blit(player.surf, player.rect)

    pygame.display.flip()