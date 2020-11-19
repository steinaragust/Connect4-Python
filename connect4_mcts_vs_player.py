import numpy as np
import random
import pygame
import sys
import math
import mcts_agent
import connect4
import copy

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

agent1_param = {'name': 'mc_AZ', 'advanced': True, 'simulations': 150, 'explore': 0}

agent = mcts_agent.MCTSAgent(agent1_param)

game = connect4.Connect4()
game_over = False

pygame.init()

SQUARESIZE = 100

width = game.COLUMN_COUNT * SQUARESIZE
height = (game.ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)


def draw_board(board):
    for c in range(game.COLUMN_COUNT):
        for r in range(game.ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(game.COLUMN_COUNT):
        for r in range(game.ROW_COUNT):
            if board[r][c] == game.PLAYER_1_PIECE:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == game.PLAYER_2_PIECE:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


screen = pygame.display.set_mode(size)
draw_board(game.get_board())
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

print(game.PLAYER_1)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if game.PLAYER_1 == game.get_to_move():
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # print(event.pos)
            # Ask for Player 1 Input
            if game.PLAYER_1 == game.get_to_move():
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if game.is_valid_location(col):
                    game.drop_piece_in_column(col)

                    if game.winning_move():
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

                    draw_board(game.get_board())

    # # Ask for Player 2 Input
    if game.get_to_move() == game.PLAYER_2 and not game_over:

        values = agent.play(copy.deepcopy(game))

        if game.is_valid_location(values[0]):
            # pygame.time.wait(500)
            game.drop_piece_in_column(values[0])

            if game.winning_move():
                label = myfont.render("Player 2 wins!!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True

            draw_board(game.get_board())

    if game_over:
        pygame.time.wait(3000)
