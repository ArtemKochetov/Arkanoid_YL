import pygame
import os

WIDTH, HEIGHT = 1600, 900
pygame.init()
pygame.display.set_caption('Red project')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
CHARACTER = None


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


pygame.display.set_icon(load_image('icon.jpg'))
read_file = open('data/saves.txt', 'rt', encoding='utf-8').readlines()
characters = {"В. И. Ленин": load_image('len.jpg'), "И. В. Сталин": load_image('stal.jpg'),
              "Л. Д. Троцкий": load_image('troc.jpg'), "А. Свердлов": load_image('sver.jpg'),
              "Николай II": load_image('nik.jpg')}


def start():
    x = 20
    font = pygame.font.Font(None, 50)
    text = ["В. И. Ленин", "И. В. Сталин", "Л. Д. Троцкий", "А. Свердлов", "Николай II"]
    string_rendered = font.render("1917 год", True, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 20
    intro_rect.x = 720
    screen.blit(string_rendered, intro_rect)
    string_rendered = font.render("Товарищ, грядёт революция. Чью сторону займёшь ты?", True, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 120
    intro_rect.x = 320
    screen.blit(string_rendered, intro_rect)
    string_rendered = font.render("Нажми на портрет", True, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 700
    intro_rect.x = 650
    screen.blit(string_rendered, intro_rect)
    for i in text:
        screen.fill(pygame.Color('gold'), (x - 5, 200 - 5, 290, 360))
        sur = pygame.transform.scale(characters[i], (280, 350))
        screen.blit(sur, (x, 200))
        string_rendered = font.render(i, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 560
        intro_rect.x = x + 30
        screen.blit(string_rendered, intro_rect)
        x += 320
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global running
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 15 < event.pos[0] < 1525 and 195 < event.pos[1] < 565:
                    global CHARACTER
                    if 15 < event.pos[0] < 305:
                        CHARACTER = 'В. И. Ленин'
                    elif 320 < event.pos[0] < 610:
                        CHARACTER = 'И. В. Сталин'
                    elif 625 < event.pos[0] < 915:
                        CHARACTER = 'Л. Д. Троцкий'
                    elif 930 < event.pos[0] < 1220:
                        CHARACTER = 'А. Свердлов'
                    elif 1235 < event.pos[0] < 1525:
                        CHARACTER = 'Николай II'
                    global not_started
                    not_started = False
                    return None


clock = pygame.time.Clock()
running = True
not_started = True
while running:
    if not_started:
        start()
    else:
        screen.fill((1, 1, 1))
        screen.blit(pygame.transform.scale(characters[CHARACTER], (280, 350)), (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(60)
    pygame.display.flip()
pygame.quit()
