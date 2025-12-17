from xiangqi.core.board import Board
from .scenes import Scene
import pygame
from xiangqi.core.const import rc_to_i
class PlayScene(Scene):
    def on_enter(self, **kwards):
        self.board = Board.initial() # 初始化棋盘一次即可
        self.inset = {"l":0.07, "r":0.06, "t":0.09, "b":0.10} # 棋盘内边距比例/微调过后

    def handle_event(self, event):
        return super().handle_event(event)

    def update(self, dt):
        return super().update(dt)

    def draw(self, screen: pygame.Surface):
        bg = self.game.assets.bg
        screen_w, screen_h = screen.get_size()
        bg_w, bg_h = bg.get_size()
        scale= max(screen_w / bg_w, screen_h / bg_h)

        new_w, new_h = int(bg_w * scale), int(bg_h * scale)
        bg_scaled = pygame.transform.smoothscale(bg, (new_w, new_h))
        bg_x, bg_y= (screen_w - new_w) // 2, (screen_h - new_h) // 2
        screen.blit(bg_scaled, (bg_x, bg_y))

        # 棋盘
        board_bg = self.game.assets.board_bg
        grid_w = int(screen_w * 0.8)
        grid_h = int(grid_w * 9 / 8)

        if grid_h > screen_h * 0.8:
            grid_h = int(screen_h * 0.8)
            grid_w = int(grid_h * 8 / 9)

        board_w = int(grid_w * 1.125)
        board_h = int(grid_h * 1.125)

        board_x = (screen_w - board_w) // 2
        board_y = (screen_h - board_h) // 2

        board_bg_scaled = pygame.transform.smoothscale(board_bg, (board_w, board_h))
        screen.blit(board_bg_scaled, (board_x, board_y))

        # 棋盘格子区域
        # 交叉点区域
        l = int(self.inset["l"] * board_w)
        r = int(self.inset["r"] * board_w)
        t = int(self.inset["t"] * board_h)
        b = int(self.inset["b"] * board_h)
        self.grid_rect = pygame.Rect(
            board_x + l,
            board_y + t,
            board_w - l - r,
            board_h - t - b
        )

        self.dx = self.grid_rect.width / 8
        self.dy = self.grid_rect.height / 9

        # 调试用 外框红色矩阵 + 棋盘绿色交叉网格点
        pygame.draw.rect(screen, (255,0,0), self.grid_rect, 2)
        for row in range(10):
            for col in range(9):
                x = self.grid_rect.left + col * self.dx
                y = self.grid_rect.top + row * self.dy
                pygame.draw.circle(screen, (0,255,0), (int(x), int(y)), 3)

        self.draw_pieces(screen)

    def draw_pieces(self, screen):
        piece_size = int(min(self.dx, self.dy) * 0.9)
        for row in range(10):
            for col in range(9):
                piece_code = self.board.squares[rc_to_i(row, col)]
                if piece_code == 0:
                    continue
                x = self.grid_rect.left + col * self.dx
                y = self.grid_rect.top + row * self.dy

                piece_img = self.game.assets.get_piece_image(piece_code)
                img_scaled = pygame.transform.smoothscale(piece_img, (piece_size, piece_size))
                rect = img_scaled.get_rect(center=(int(x), int(y)))
                screen.blit(img_scaled, rect)


