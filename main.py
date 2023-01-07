import pygame
from random import choice
import os

WIDTH = 1000
HEIGHT = 1000
pygame.init()
pygame.display.set_caption('Arkanoid')
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Ball(pygame.sprite.Sprite):
    image = load_image('ball.png', -1)
    image = pygame.transform.scale(image, (50, 50))

    def __init__(self, group):
        super().__init__(group)
        self.image = Ball.image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - 75
        self.rect.y = HEIGHT - 120
        self.speed_x = 1
        self.speed_y = -1
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, other):
        if pygame.sprite.collide_mask(self, other):
            self.speed_x = choice((-1, 0, 1))
            self.speed_y *= -1


class Paddle(pygame.sprite.Sprite):
    image = load_image('paddle.png')
    image = pygame.transform.scale(image, (125, 20))

    def __init__(self, group):
        super().__init__(group)
        self.image = Paddle.image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - 125
        self.rect.y = HEIGHT - 40
        self.speed = 1
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, event):
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.speed = -1
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.speed = 1


class Bar(pygame.sprite.Sprite):

    def __init__(self, group, img, x, y, price):
        super().__init__(group)
        image = load_image(img)
        self.image = pygame.transform.scale(image, (100, 65))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.price = abs(price - 3) * 10


paddle_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
bars_group = pygame.sprite.Group()


class Game:
    def __init__(self):
        self.bar_y = 100
        self.bars_not_drawed = True
        self.ball = Ball(ball_group)
        self.paddle = Paddle(paddle_group)
        self.score = 0
        self.fon_img = load_image('fon_img.jpg')

    def render(self, screen):
        screen.blit(self.fon_img, (0, 0))
        if self.paddle.rect.x == 0 or self.paddle.rect.x == 875:
            self.paddle.speed *= -1
        if self.ball.rect.x == 0 or self.ball.rect.x == 950:
            self.ball.speed_x *= -1
        if self.ball.rect.y == 0:
            self.ball.speed_y *= -1
            self.ball.speed_x = choice((-1, 0, 1))
        self.paddle.rect.x += self.paddle.speed
        self.ball.update(self.paddle)
        if self.bars_not_drawed:
            self.draw_bars(screen)
            self.bars_not_drawed = False
        for bar in bars_group:
            if pygame.sprite.collide_mask(self.ball, bar):
                self.score += bar.price
                self.ball.update(bar)
                bars_group.remove(bar)
        self.ball.rect.x += self.ball.speed_x
        self.ball.rect.y += self.ball.speed_y
        ball_group.draw(screen)
        paddle_group.draw(screen)
        bars_group.draw(screen)

    def draw_bars(self, screen):
        bar_y = 100
        colors = ['блок2.png', 'блок1.png', 'блок3.png']
        for color in colors:
            bar_x = 30
            for i in range(9):
                Bar(bars_group, color, bar_x, bar_y, colors.index(color))
                bar_x += 105
            bar_y += 70


def start_screen():
    img = pygame.transform.scale(load_image('start_screen.jpg'), (1000, 1000))
    mode = 1
    with open('data/рекорд.txt', 'r') as read_file:
        record = int([line.strip() for line in read_file][0])
        read_file.close()
    intro_text = [f"Твой рекорд: {record}"]
    font = pygame.font.Font(None, 50)
    while True:
        screen.blit(img, (0, 0))
        string_rendered = font.render(intro_text[0], True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 620
        intro_rect.x = 430
        screen.blit(string_rendered, intro_rect)
        if mode == 1:
            pygame.draw.rect(screen, pygame.Color('yellow'), (70, 460, 205, 70), 5, 5, )
        elif mode == 2:
            pygame.draw.rect(screen, pygame.Color('yellow'), (345, 460, 270, 70), 5, 5, )
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT or event.key == pygame.K_2:
                    mode = 2
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT or event.key == pygame.K_1:
                    mode = 1
                elif event.key == pygame.K_RETURN:
                    return mode, record
        pygame.display.flip()


def end_screen(score):
    img = pygame.transform.scale(load_image('end_screen.jpg'), (1000, 1000))
    screen.blit(img, (0, 0))
    intro_text = ["Игра окончена.",
                  f"Твой результат: {score}",
                  "Чтобы играть снова нажми",
                  "на Пробел или Enter."]
    screen.blit(img, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 460
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 440
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                play()
        pygame.display.flip()


def play():
    pygame.mouse.set_visible(False)
    game_mode, record = start_screen()
    clock = pygame.time.Clock()
    ticks = 0
    speed = 10
    count = 0
    running = True
    playing = True
    ark = Game()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                playing = not playing
            if playing:
                if event.type == pygame.KEYDOWN:
                    ark.paddle.move(event)
        if playing:
            ark.render(screen)
            pygame.display.flip()
        if ticks >= speed:
            if playing:
                ark.render(screen)
                ticks = 0
        if ark.ball.rect.y > 1000:
            running = False
        if ark.score == 540:
            if game_mode == 1:
                running = False
            if game_mode == 2:
                count += 1
                ark.score = 0
                ark.bars_not_drawed = True
        clock.tick(250)
        ticks += 1
    if ark.score > record:
        with open('data/рекорд.txt', 'w') as write_file:
            write_file.write(str(ark.score))
            write_file.close()
    paddle_group.remove(ark.paddle)
    ball_group.remove(ark.ball)
    bars_group.clear(screen, screen)
    end_screen(ark.score + 540 * count)


play()
pygame.quit()
