import pygame
import os
import sys


#def load_image(name, colorkey=None):
    #fullname = os.path.join(name)
    #image = pygame.image.load(fullname)
    #return image


class Board:
    def draw_platform(self, screen, x_pos):
        pygame.draw.rect(screen, pygame.Color((8, 218, 242)), (x_pos, 315, 140, 30))

    def draw_ball(self, screen, y_pos):
        ball = pygame.draw.circle(screen, pygame.Color('white'), (int(y_pos), int(y_pos)), 15)


class Level1(Board):
    def draw_bricks(self, screen):
        width = 5
        width2 = 5
        for _ in range(6):
            pygame.draw.rect(screen, pygame.Color((255, 128, 0)), (width, 60, 90, 25))
            width += 100
        for _ in range(6):
            pygame.draw.rect(screen, pygame.Color((111, 255, 0)), (width2, 30, 90, 25))
            width2 += 100


if __name__ == '__main__':
    pygame.init()
    size = width, height = 600, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('ARKANOID')
    #img = load_image('fon arkanoid.jpg')
    x_pos = 240
    y_pos = 300
    v = 60
    fps = 165
    clock = pygame.time.Clock()
    while pygame.event.wait().type != pygame.QUIT:
        board = Board()
        level1 = Level1()
        running = True
        while running:
            #screen.blit(img, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                #if event.type == pygame.MOUSEBUTTONDOWN:

                if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                    x_pos -= 50
                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    x_pos += 50
            y_pos -= v / fps
            screen.fill((0, 0, 0))
            board.draw_platform(screen, x_pos)
            level1.draw_bricks(screen)
            board.draw_ball(screen, y_pos)
            clock.tick(fps)
            pygame.display.flip()
    pygame.quit()