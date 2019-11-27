# -*- coding: utf8 -*-
import pygame
from random import randint


pygame.init()
NET_COLOR = (0, 0, 0)
COLORS = [(255, 204, 0), (255, 255, 0), (102, 0, 255), (31, 174, 233), (0, 155, 118),
          (236, 235, 189), (218, 189, 171), (102, 153, 204), (28, 84, 45),
          (205, 127, 50), (255, 36, 0)]
BACKGROUND_COLOR = (0, 255, 255)
FIGURAS = [(((0, 2), (1, 2), (2, 2), (3, 2)), ((1, 0), (1, 1), (1, 2), (1, 3)), ((3, 1), (2, 1), (1, 1), (0, 1)), ((2, 3), (2, 2), (2, 1), (2, 0))),
(((0, 0), (0, 1), (1, 0), (2, 0)), ((2, 0), (1, 0), (2, 1), (2, 2)), ((2, 2), (2, 1), (1, 2), (0, 2)), ((0, 2), (1, 2), (0, 1), (0, 0))),
(((0, 1), (0, 2), (1, 2), (2, 2)), ((1, 0), (0, 0), (0, 1), (0, 2)), ((2, 1), (2, 0), (1, 0), (0, 0)), ((1, 2), (2, 2), (2, 1), (2, 0))),
(((0, 0), (0, 1), (1, 1), (1, 0))),
(((0, 2), (1, 2), (1, 1), (2, 1)), ((0, 0), (0, 1), (1, 1), (1, 2)), ((2, 0), (1, 0), (1, 1), (0, 1)), ((2, 2), (2, 1), (1, 1), (1, 0))),
(((0, 1), (1, 1), (1, 2), (2, 2)), ((1, 0), (1, 1), (0, 1), (0, 2)), ((2, 1), (1, 1), (1, 0), (0, 0)), ((1, 2), (1, 1), (2, 1), (2, 0))),
(((1, 0), (1, 1), (1, 2), (0, 1)), ((2, 1), (1, 1), (0, 1), (1, 0)), ((1, 2), (1, 1), (1, 0), (2, 1)), ((0, 1), (1, 1), (2, 1), (1, 2)))]
PRIORITIES = [10, 15, 15, 10, 15, 15, 20]


class Cell:
    def __init__(self, color):
        self.color = pygame.Color(*color)
    
    def get_color(self):
        return self.color
        

class Tetris:
    def __init__(self, width, height, left, top, cell_size):
        self.cell_size = cell_size
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.score = 0
        self.figura_x = -1
        self.figura_y = -1
        self.figura = None
        self.figura_color = None
        self.board = []
        self.falling_figura = -1
        for i in range(height + 4):
            self.board.append([None] * width)
        self.new_figura()
    
    def render_board(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, NET_COLOR, (left + j * self.cell_size,
                                                     left + i * self.cell_size, self.cell_size, self.cell_size), 2)
    
    def new_figura(self):
        num = randint(0, 100)
        now_sum = 0
        for i in range(len(PRIORITIES)):
            if now_sum < PRIORITIES[i]
        minx = -100000
        maxx = 100000
        y = 100000
        for i in figura:
            minx = max(minx, -i[1])
            maxx = min(maxx, self.width - i[1] - 1)
            y = min(y, 3 - i[0])
        self.figura = figura
        self.figura_y = y
        self.figura_x = randint(minx, maxx)
        self.figura_color = COLORS[randint(0, len(COLORS) - 1)]
        self.draw_figura_on_board()
    
    def draw_figura_on_board(self):
        for i in self.figura:
            self.board[i[0] + self.figura_y][i[1] + self.figura_x] = Cell(self.figura_color)
    
    def delete_figura_from_board(self):
        for i in self.figura:
            self.board[i[0] + self.figura_y][i[1] + self.figura_x] = None
    
    def rotate(self):
        new_figura = None
        for i in FIGURAS:
            ok = False
            for j in range(len(i)):
                if i[j] == self.figura:
                    new_figura = i[(j + 1) % len(i)]
                    of = True
                    break
            if ok:
                break
        ok = True
        self.delete_figura_from_board()
        for i in new_figura:
            if i[0] + self.figura_y < 0 or i[0] + self.figura_y > self.height + 3:
                ok = False
                break
            if i[1] + self.figura_x < 0 or i[1] + self.figura_x > self.width - 1:
                ok = False
                break                
            if self.board[i[0] + self.figura_y][i[1] + self.figura_x] is not None:
                ok = False
                break
        if ok:
            self.figura = new_figura
        self.draw_figura_on_board()
    
    def move(self, step):
        if abs(step) > 1:
            return
        new_x = self.figura_x + step
        ok = True
        self.delete_figura_from_board()
        for i in self.figura:
            if i[0] + self.figura_y < 0 or i[0] + self.figura_y > self.height + 3:
                ok = False
                break
            if i[1] + new_x < 0 or i[1] + new_x > self.width - 1:
                ok = False
                break                
            if self.board[i[0] + self.figura_y][i[1] + new_x] is not None:
                ok = False
                break
        if ok:
            self.figura_x = new_x
        self.draw_figura_on_board()
    
    def tick(self):
        new_y = self.figura_y + 1
        ok = True
        self.delete_figura_from_board()
        for i in self.figura:
            if i[0] + new_y < 0 or i[0] + new_y > self.height + 3:
                ok = False
                break
            if i[1] + self.figura_x < 0 or i[1] + self.figura_x > self.width - 1:
                ok = False
                break                
            if self.board[i[0] + new_y][i[1] + self.figura_x] is not None:
                ok = False
                break
        if ok:
            self.figura_y = new_y
            self.draw_figura_on_board()
        else:
            self.draw_figura_on_board()
            self.new_figura()