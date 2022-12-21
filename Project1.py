import pygame
import random
import os
import sys

pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Bricks(pygame.sprite.Sprite):
    image1 = load_image("red_brick.png")
    image2 = load_image("purple_brick.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image1 = Bricks.image1
        self.image2 = Bricks.image2
        self.rect1 = self.image1.get_rect()
        self.rect2 = self.image2.get_rect()
        self.mask1 = pygame.mask.from_surface(self.image1)
        self.mask2 = pygame.mask.from_surface(self.image2)
        self.rect1.bottom = height
        self.rect2.bottom = height


class Platform(pygame.sprite.Sprite):
    image = load_image("platform.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Platform.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.bottom = height
        self.paddle_x = width // 2 - 125

    def update(self, event):
        if event.key == pygame.K_LEFT and self.paddle_x > 0:
            self.paddle_speed = -1
        elif event.key == pygame.K_RIGHT:
            self.paddle_speed = 1


class Ball(pygame.sprite.Sprite):
    image = load_image("ball_arkanoid.png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Ball.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        if not pygame.sprite.collide_mask(self, platform):
            self.rect = self.rect.move((1 * -1), (1 * -1))
        else:
            self.rect = self.rect.move((-1 * -1), (1 * -1))
        if not pygame.sprite.collide_mask(self, bricks):
            self.rect = self.rect.move((1 * -1), (1 * -1))
        else:
            self.rect = self.rect.move((-1 * -1), (-1 * -1))


size = width, height = 800, 600
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
ticks = 0
speed = 10
bricks = Bricks()
platform = Platform()
playing = True
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            Ball(event.pos)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            playing = not playing
        if event.type == pygame.KEYDOWN:
            platform.update(event)
    if playing:
        pygame.display.flip()
    if ticks >= speed:
        if playing:
            ticks = 0

    all_sprites.update()
    screen.fill(pygame.Color('white'))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(100)
    ticks += 1
pygame.quit()