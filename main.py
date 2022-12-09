import pygame
from copy import deepcopy


class Board:
    # создание поля
    def __init__(self, width, height, left=10, top=10, cell_size=20):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = 0
        self.set_view(left, top, cell_size)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size


class Life(Board):
    def __init__(self, width, height, left=10, top=10, cell_size=20):
        super().__init__(width, height, left=10, top=10, cell_size=20)

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x]:
                    pygame.draw.rect(screen, pygame.Color((20, 200, 20)), (x * self.cell_size + self.left,
                                     y * self.cell_size + self.top, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, pygame.Color((20, 20, 20)), (x * self.cell_size + self.left,
                                                                      y * self.cell_size + self.top,
                                                                      self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        return x, y

    def on_click(self, cell_coords):
        self.board[cell_coords[1]][cell_coords[0]] = (self.board[cell_coords[1]][cell_coords[0]] + 1) % 2

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def next_move(self):
        new_board = deepcopy(self.board)
        for y in range(self.height):
            for x in range(self.width):
                s = 0
                for delta_y in range(-1, 2):
                    for delta_x in range(-1, 2):
                        if self.width <= x + delta_x or x + delta_x < 0 or \
                                self.height <= y + delta_y or y + delta_y < 0:
                            continue
                        s += self.board[y + delta_y][x + delta_x]
                    s -= self.board[y][x]
                    if s == 3:
                        new_board[y][x] = 1
                    elif s < 2 or s > 3:
                        new_board[y][x] = 0
        self.board = deepcopy(new_board)


pygame.init()
screen = pygame.display.set_mode((600, 600))
board = Life(29, 29, 10, 10, 30)
clock = pygame.time.Clock()
ticks = 0
speed = 10
life_going = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            board.get_click(event.pos)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or \
                event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            life_going = not life_going
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            speed += 1
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            speed -= 1
        screen.fill((235, 235, 235))
        board.render(screen)
        if ticks >= speed:
            if life_going:
                board.next_move()
            ticks = 0
        pygame.display.flip()
        clock.tick(100)
        ticks += 1
pygame.quit()
