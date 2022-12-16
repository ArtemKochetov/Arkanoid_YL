import pygame
from random import choice

WIDTH = 1200
HEIGHT = 800


class Game:

    def __init__(self):
        self.paddle_speed = 1
        self.paddle_x = WIDTH // 2 - 125
        self.ball_x = WIDTH // 2
        self.ball_y = HEIGHT - 100
        self.bar_y = 100
        self.bars = []
        self. ball_speed_y = 1
        self.ball_speed_x = 1
        self.bars_not_drawed = True
        self.ball = pygame.Rect((self.ball_x, self.ball_y, 40, 40))
        self.paddle = pygame.Rect((self.paddle_x, HEIGHT - 40, 250, 30))

    def draw(self, screen):
        if self.paddle_x == 0 or self.paddle_x == 950:
            self.paddle_speed *= -1
        if self.paddle.colliderect(self.ball):
            self.ball_speed_y *= -1
            self.ball_speed_x *= choice([-1, 1])
        screen.fill((1, 1, 1))
        self.paddle_x += self.paddle_speed
        self.update_ball()
        self.ball = pygame.Rect((self.ball_x, self.ball_y, 40, 40))
        self.paddle = pygame.Rect((self.paddle_x, HEIGHT - 40, 250, 30))
        pygame.draw.rect(screen, pygame.Color('orange'), self.ball)
        pygame.draw.rect(screen, pygame.Color('darkorange'), self.paddle)
        if self.bars_not_drawed:
            self.draw_bars(screen)
            self.bars_not_drawed = False
        for bar in self.bars:
            pygame.draw.rect(screen, bar[1], bar[0])

    def update(self, event):
        if event.key == pygame.K_LEFT and self.paddle_x > 0:
            self.paddle_speed = -1
        elif event.key == pygame.K_RIGHT:
            self.paddle_speed = 1

    def update_ball(self):
        self.ball_y -= self.ball_speed_y
        self.ball_x += self.ball_speed_x
        if self.ball_x >= WIDTH - 40 or self.ball_x <= 0:
            self.ball_speed_x *= -1
        if self.ball_y <= 0:
            self.ball_speed_y *= -1
        for bar in self.bars:
            if self.ball.colliderect(bar[0]):
                self.bars.remove(bar)
                self.ball_speed_y *= -1
                self.ball_speed_x *= choice([-1, 1])

    def draw_bars(self, screen):
        bar_y = 100
        for color in ['red', 'lightblue', 'green']:
            bar_x = 55
            for i in range(8):
                bar = [(pygame.Rect(bar_x, bar_y, 110, 50)), color]
                self.bars.append(bar)
                bar_x += 140
            bar_y += 70


pygame.init()
pygame.display.set_caption('Arkanoid')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
ticks = 0
speed = 10
running = True
playing = True
ark = Game()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            playing = not playing
        if event.type == pygame.KEYDOWN:
            ark.update(event)
    if playing:
        ark.draw(screen)
        pygame.display.flip()
    if ticks >= speed:
        if playing:
            ark.draw(screen)
            ticks = 0
    pygame.display.flip()
    clock.tick(200)
    ticks += 1
pygame.quit()
