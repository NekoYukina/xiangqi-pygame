from .scenes import Scene
from .game_config import SQUARE_SIZE
import pygame
class PlayScene(Scene):
    def on_enter(self, **kwards):
        return super().on_enter(**kwards)

    def handle_event(self, event):
        return super().handle_event(event)

    def update(self, dt):
        return super().update(dt)

    def draw(self, screen: pygame.Surface):
        bg = self.game.assets.bg
        screen_w, screen_h = screen.get_size()
        bg_w, bg_h = bg.get_size()

        scale_x, scale_y= screen_w / bg_w, screen_h / bg_h
        scale = max(scale_x, scale_y)
        new_w = int(bg_w * scale)
        new_h = int(bg_h * scale)
        bg_scaled = pygame.transform.smoothscale(bg, (new_w, new_h))
        bg_x, bg_y= (screen_w - new_w) // 2, (screen_h - new_h) // 2
        screen.blit(bg_scaled, (bg_x, bg_y))

        board_width = int(screen_w * 0.8)
        board_height = int(board_width * 10 / 9)

        if board_width > screen_h * 0.9:
            board_height = int(screen_h * 0.8)
            board_width = int(board_height * 9 / 10)

        self.square_size = board_width // 9
        board_bg = self.game.assets.board_bg
        board_bg_scaled = pygame.transform.smoothscale(board_bg, (board_width, board_height))
        board_x = (screen_w - board_width) // 2
        board_y = (screen_h - board_height) // 2
        screen.blit(board_bg_scaled, (board_x, board_y))


