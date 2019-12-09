# -*- coding: utf8 -*-
import pygame
from random import randint
import os
import sqlite3
import datetime


pygame.init()
NET_COLOR = (0, 0, 0)
COLORS = [(255, 204, 0), (255, 255, 0), (102, 0, 255), (31, 174, 233), (0, 155, 118),
          (236, 235, 189), (218, 189, 171), (102, 153, 204), (205, 127, 50),
          (255, 36, 0)]
PLAY = 0
RULES = 1
QUIT = 2
BACKGROUND_COLOR = (0, 90, 90)
BACKGROUND_FIGURA_COLOR = (200, 200, 200)
TEXT_COLOR = (255, 100, 20)
CHOSEN_TEXT_COLOR = (200, 200, 200)
FIGURAS = [(((0, 2), (1, 2), (2, 2), (3, 2)), ((1, 0), (1, 1), (1, 2), (1, 3)),
            ((3, 1), (2, 1), (1, 1), (0, 1)), ((2, 3), (2, 2), (2, 1), (2, 0))),
           (((0, 1), (0, 2), (1, 1), (2, 1)), ((1, 0), (0, 0), (1, 1), (1, 2)), ((2, 1), (2, 0),
            (1, 1), (0, 1)), ((1, 2), (2, 2), (1, 1), (1, 0))),
           (((0, 0), (0, 1), (1, 1), (2, 1)), ((2, 0), (1, 0), (1, 1), (1, 2)), ((2, 2), (2, 1),
            (1, 1), (0, 1)), ((0, 2), (1, 2), (1, 1), (1, 0))),
           (((0, 0), (0, 1), (1, 1), (1, 0)),),
           (((0, 2), (1, 2), (1, 1), (2, 1)), ((0, 0), (0, 1), (1, 1), (1, 2)), ((2, 0), (1, 0),
            (1, 1), (0, 1)), ((2, 2), (2, 1), (1, 1), (1, 0))),
           (((0, 1), (1, 1), (1, 2), (2, 2)), ((1, 0), (1, 1), (0, 1), (0, 2)), ((2, 1), (1, 1),
            (1, 0), (0, 0)), ((1, 2), (1, 1), (2, 1), (2, 0))),
           (((1, 0), (1, 1), (1, 2), (0, 1)), ((2, 1), (1, 1), (0, 1), (1, 0)), ((1, 2), (1, 1),
            (1, 0), (2, 1)), ((0, 1), (1, 1), (2, 1), (1, 2)))]
PRIORITIES = [15, 15, 15, 10, 15, 15, 15]


class Cell:
    def __init__(self, color):
        self.color = pygame.Color(*color)
    
    def get_color(self):
        return self.color


class EndAnimation(pygame.sprite.Sprite):
    image = pygame.image.load(os.path.join('data', 'gameover.jpg'))
    
    def __init__(self, group):
        super().__init__(group)
        self.image = EndAnimation.image
        self.rect = self.image.get_rect()
        self.rect.y = -500
    
    def update(self):
        if self.rect.y < 0:
            self.rect.y += 1


class StartMenu:
    def __init__(self, width, top, delta_y, font_size):
        self.chosen = 0
        self.width = width
        self.left = width // 2
        self.top = top
        self.delta_y = delta_y
        self.font_size = font_size
    
    def render(self, screen):
        screen.fill(BACKGROUND_COLOR)
        font = pygame.font.Font(os.path.join('data', 'shrift.ttf'), self.font_size)
        if self.chosen != 0:
            text = font.render("Play!", 1, TEXT_COLOR)
        else:
            text = font.render("Play!", 1, CHOSEN_TEXT_COLOR)
        text_x = self.left - text.get_width() // 2
        text_y = self.top - text.get_height() // 2
        screen.blit(text, (text_x, text_y))
        
        font = pygame.font.Font(os.path.join('data', 'shrift.ttf'), self.font_size)
        if self.chosen != 1:
            text = font.render("Author", 1, TEXT_COLOR)
        else:
            text = font.render("Author", 1, CHOSEN_TEXT_COLOR)
        text_x = self.left - text.get_width() // 2
        text_y = self.top - text.get_height() // 2 + self.delta_y
        screen.blit(text, (text_x, text_y))
        
        font = pygame.font.Font(os.path.join('data', 'shrift.ttf'), self.font_size)
        if self.chosen != 2:
            text = font.render("Quit", 1, TEXT_COLOR)
        else:
            text = font.render("Quit", 1, CHOSEN_TEXT_COLOR)
        text_x = self.left - text.get_width() // 2
        text_y = self.top - text.get_height() // 2 + self.delta_y * 2
        screen.blit(text, (text_x, text_y))
    
    def click(self, pos):
        font = pygame.font.Font(os.path.join('data', 'shrift.ttf'), self.font_size)
        text = font.render("Play!", 1, (0, 0, 0))
        text_x = self.left - text.get_width() // 2
        text_y = self.top - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        if pos[0] <= text_x + text_w and pos[0] >= text_x:
            if pos[1] <= text_y + text_h and pos[1] >= text_y:
                self.chosen = 0
                return PLAY
        
        font = pygame.font.Font(os.path.join('data', 'shrift.ttf'), self.font_size)
        text = font.render("Author", 1, (0, 0, 0))
        text_x = self.left - text.get_width() // 2
        text_y = self.top - text.get_height() // 2 + self.delta_y
        text_w = text.get_width()
        text_h = text.get_height()
        if pos[0] <= text_x + text_w and pos[0] >= text_x:
            if pos[1] <= text_y + text_h and pos[1] >= text_y:
                self.chosen = 1
                return RULES
        
        font = pygame.font.Font(os.path.join('data', 'shrift.ttf'), self.font_size)
        text = font.render("Quit", 1, (0, 0, 0))
        text_x = self.left - text.get_width() // 2
        text_y = self.top - text.get_height() // 2 + self.delta_y * 2
        text_w = text.get_width()
        text_h = text.get_height()
        if pos[0] <= text_x + text_w and pos[0] >= text_x:
            if pos[1] <= text_y + text_h and pos[1] >= text_y:
                self.chosen = 2
                return QUIT
    
    def mouse_move(self, pos):
        font = pygame.font.Font(os.path.join('data', 'shrift.ttf'), self.font_size)
        text = font.render("Play!", 1, (0, 0, 0))
        text_x = self.left - text.get_width() // 2
        text_y = self.top - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        if pos[0] <= text_x + text_w and pos[0] >= text_x:
            if pos[1] <= text_y + text_h and pos[1] >= text_y:
                self.chosen = 0
        
        font = pygame.font.Font(os.path.join('data', 'shrift.ttf'), self.font_size)
        text = font.render("Author", 1, (0, 0, 0))
        text_x = self.left - text.get_width() // 2
        text_y = self.top - text.get_height() // 2 + self.delta_y
        text_w = text.get_width()
        text_h = text.get_height()
        if pos[0] <= text_x + text_w and pos[0] >= text_x:
            if pos[1] <= text_y + text_h and pos[1] >= text_y:
                self.chosen = 1
        
        font = pygame.font.Font(os.path.join('data', 'shrift.ttf'), self.font_size)
        text = font.render("Quit", 1, (0, 0, 0))
        text_x = self.left - text.get_width() // 2
        text_y = self.top - text.get_height() // 2 + self.delta_y * 2
        text_w = text.get_width()
        text_h = text.get_height()
        if pos[0] <= text_x + text_w and pos[0] >= text_x:
            if pos[1] <= text_y + text_h and pos[1] >= text_y:
                self.chosen = 2
    
    def key_up(self, key):
        if key == 273:
            self.chosen = (self.chosen - 1) % 3
        elif key == 274:
            self.chosen = (self.chosen + 1) % 3
        elif key == 13:
            return self.chosen
        

class TetrisBoard:
    def __init__(self, width, height, left, top, cell_size, next_left, next_top,
                 score_top, score_left, font_size):
        self.con = sqlite3.connect(os.path.join('data', 'results.db'))
        self.font_size = font_size
        self.score = 0
        self.score_left = score_left
        self.score_top = score_top  
        self.next_top = next_top
        self.next_left = next_left
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
        num = randint(0, 100)
        now_sum = 0
        next_figura = None
        for i in range(len(PRIORITIES)):
            now_sum += PRIORITIES[i]
            if now_sum >= num:
                next_figura = FIGURAS[i][randint(0, len(FIGURAS[i]) - 1)]
                break
        self.next_figura = next_figura
        self.next_figura_color = COLORS[randint(0, len(COLORS) - 1)]
        self.new_figura()
    
    def render(self, screen):
        screen.fill(BACKGROUND_COLOR)
        self.render_next_figura(screen)
        self.render_board(screen)
        self.render_score(screen)
    
    def render_board(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, NET_COLOR, (self.left + j * self.cell_size,
                                                     self.top + i * self.cell_size,
                                                     self.cell_size, self.cell_size), 1)
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i + 4][j] is not None:
                    pygame.draw.rect(screen, self.board[i + 4][j].get_color(),
                                     (self.left + j * self.cell_size + 1,
                                      self.top + i * self.cell_size + 1,
                                      self.cell_size - 2, self.cell_size - 2))
    
    def render_score(self, screen):
        font = pygame.font.Font(os.path.join('data', 'shrift.ttf'), self.font_size)
        text = font.render("Score: " + str(self.score), 1, TEXT_COLOR)
        text_x = self.score_left
        text_y = self.score_top
        screen.blit(text, (text_x, text_y))
    
    def render_score_x_y(self, screen, x, y):
        font = pygame.font.Font(os.path.join('data', 'shrift.ttf'), self.font_size)
        text = font.render("Score: " + str(self.score), 1, TEXT_COLOR)
        text_x = x - text.get_width() // 2
        text_y = y - text.get_height() // 2
        screen.blit(text, (text_x, text_y))        
    
    def render_next_figura(self, screen):
        pygame.draw.rect(screen, BACKGROUND_FIGURA_COLOR, (self.next_left + 1,
                                                           self.next_top + 1, 5 * self.cell_size - 2,
                                                           5 * self.cell_size - 2))        
        pygame.draw.rect(screen, NET_COLOR, (self.next_left, self.next_top, 5 * self.cell_size,
                                             5 * self.cell_size), 2)
        minx = 10000
        maxx = -10000
        miny = 10000
        maxy = -10000
        for i in self.next_figura:
            minx = min(minx, i[1])
            maxx = max(maxx, i[1])
            miny = min(miny, i[0])
            maxy = max(maxy, i[0])
        dx = maxx - minx + 1
        dy = maxy - miny + 1
        dx = (5 - dx) * self.cell_size / 2
        dy = (5 - dy) * self.cell_size / 2
        for i in self.next_figura:
            pygame.draw.rect(screen, self.next_figura_color,
                             (dx + self.next_left + self.cell_size * (i[1] - minx) + 1,
                              dy + self.next_top + self.cell_size * (i[0] - miny) + 1,
                              self.cell_size - 2, self.cell_size - 2))
            pygame.draw.rect(screen, NET_COLOR,
                             (dx + self.next_left + self.cell_size * (i[1] - minx),
                              dy + self.next_top + self.cell_size * (i[0] - miny),
                              self.cell_size, self.cell_size), 1)            
    
    def new_figura(self):
        figura = self.next_figura
        self.figura_color = self.next_figura_color
        num = randint(0, 100)
        now_sum = 0
        next_figura = None
        for i in range(len(PRIORITIES)):
            now_sum += PRIORITIES[i]
            if now_sum >= num:
                next_figura = FIGURAS[i][randint(0, len(FIGURAS[i]) - 1)]
                break
        self.next_figura = next_figura
        self.next_figura_color = COLORS[randint(0, len(COLORS) - 1)]
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
                    new_figura = i[(j - 1) % len(i)]
                    ok = True
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
    
    def check_lose(self):
        for i in range(4):
            for j in range(self.width):
                if self.board[i][j] is not None:
                    return True
        return False
    
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
    
    def delete_buttom_lines(self):
        delta = 0
        for i in range(self.height + 3, self.height - 1, -1):
            ok = True
            for j in range(self.width):
                if self.board[i][j] is None:
                    ok = False
                    break
            if ok:
                delta += 1
                continue
            else:
                break
        if delta == 0:
            return
        self.score += delta * 100
        for i in range(self.height + 3, 3, -1):
            for j in range(self.width):
                if i < delta + 4:
                    self.board[i][j] = None
                else:
                    self.board[i][j] = self.board[i - delta][j]
    
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
            if self.check_lose():
                cur = self.con.cursor()
                date = datetime.datetime.now()
                time = str(date.hour) + ':' + str(date.minute)
                date = str(date.day) + '.' + str(date.month) + '.' + str(date.year)
                req = 'INSERT INTO result VALUES("' + date + '", "' + time + '", '
                req += str(self.score) + ')'
                cur.execute(req)
                self.con.commit()
                return False
            else:
                self.score += 10
                self.delete_buttom_lines()
                self.new_figura()
        return True