import pygame
from xiangqi.ui.game import Game
from xiangqi.ui.game_config import GAME_WIDTH, GAME_HEIGHT
from xiangqi.ui.playscene import PlayScene

pygame.init()
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Xiangqi Test")
game = Game(screen)
game.change_scene(PlayScene(game))
game.run()