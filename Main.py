# -*- coding: utf8 -*-
import pygame
import webbrowser
from Tetris import *


pygame.init()
arrow_file = os.path.join('data', 'arrow.png')
arrow_image = pygame.image.load(arrow_file)
screen = pygame.display.set_mode((500, 500))
running = True
game_now = False
animation = False
clock = pygame.time.Clock()
time = 0
time1 = 0
clock1 = pygame.time.Clock()
gr = None
board = TetrisBoard(10, 20, 10, 20, 22, 320, 100, 300, 250, 30)
menu = StartMenu(500, 100, 130, 80)
up = False
down = False
left = False
right = False
while running:
    if game_now:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == 273:
                    time1 = 0
                    clock1.tick()
                    board.rotate()
                    up = True
                if event.key == 274:
                    time1 = 0
                    clock1.tick()                    
                    down = True
                    time = 0
                    clock.tick()
                    board.tick()
                if event.key == 275:
                    time1 = 0
                    clock1.tick()                    
                    board.move(1)
                    right = True
                if event.key == 276:
                    time1 = 0
                    clock1.tick()                    
                    board.move(-1)
                    left = True
            if event.type == pygame.KEYUP:
                if event.key == 273:
                    up = False          
                if event.key == 274:
                    time = 0
                    clock.tick()                      
                    down = False
                if event.key == 275:
                    right = False
                if event.key == 276:
                    left = False
        time += clock.tick()
        time1 += clock1.tick()
        if time1 > 150:
            time1 = 0
            if left or right or up or down:
                if right:
                    board.move(1)
                if left:
                    board.move(-1)
                if up:
                    board.rotate()
                if down:
                    time = 0
                    game_now = board.tick()
                    if not game_now:
                        animation = True
        if time > 400:
            time = 0
            game_now = board.tick()
            if not game_now:
                animation = True
        board.render(screen)
    elif not animation:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                ret = menu.key_up(event.key)
                if ret == PLAY:
                    game_now = True
                    board = TetrisBoard(10, 20, 10, 20, 22, 320, 100, 300, 250, 50)
                if ret == QUIT:
                    running = False
                    break
                if ret == RULES:
                    webbrowser.open('https://github.com/igorfardoc')
            if event.type == pygame.MOUSEMOTION:
                menu.mouse_move(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                ret = menu.click(event.pos)
                if ret == PLAY:
                    game_now = True
                    board = TetrisBoard(10, 20, 10, 20, 22, 320, 100, 300, 250, 50)
                if ret == QUIT:
                    running = False
                    break
                if ret == RULES:
                    webbrowser.open('https://github.com/igorfardoc')
        menu.render(screen)   
    else:
        if gr is None:
            gr = pygame.sprite.Group()
            EndAnimation(gr)
            time = 0
            y = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP and event.key == 13:
                ret = menu.key_up(event.key)
                animation = False
                gr = None
                menu = StartMenu(500, 100, 130, 80)
        time += clock.tick()
        if time > 10 and animation:
            time = 0
            gr.update()
            if y < 500:
                y += 1
            gr.draw(screen)
            board.render_score_x_y(screen, 250, y - 200)
    if pygame.mouse.get_focused():
        pygame.mouse.set_visible(0)
        screen.blit(arrow_image, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
    else:
        pygame.mouse.set_visible(1)
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
    pygame.display.flip()
pygame.quit()