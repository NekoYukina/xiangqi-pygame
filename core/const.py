from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum

# 90格：r 0..9, c 0..8
BOARD_ROWS = 10
BOARD_COLS = 9
BOARD_SIZE = BOARD_ROWS * BOARD_COLS

def rc_to_i(r: int, c: int) -> int:
    return r * BOARD_COLS + c

def i_to_rc(i: int) -> tuple[int, int]:
    return divmod(i, BOARD_COLS)

class Side(IntEnum):
    RED = 1
    BLACK = -1

class Piece(IntEnum):
    EMPTY = 0
    KING = 1     # 将/帅
    ADVISOR = 2  # 士/仕
    ELEPHANT = 3 # 象/相
    ROOK = 4     # 车
    KNIGHT = 5   # 马
    CANNON = 6   # 炮
    PAWN = 7     # 兵/卒

def side_of(piece_code: int) -> Side | None:
    if piece_code > 0:
        return Side.RED
    if piece_code < 0:
        return Side.BLACK
    return None

def type_of(piece_code: int) -> Piece:
    return Piece(abs(piece_code))

# 用于文本打印（红大写，黑小写）
PIECE_CHAR = {
    0: ".",
    +Piece.KING: "K",
    +Piece.ADVISOR: "A",
    +Piece.ELEPHANT: "E",
    +Piece.ROOK: "R",
    +Piece.KNIGHT: "N",
    +Piece.CANNON: "C",
    +Piece.PAWN: "P",
    -Piece.KING: "k",
    -Piece.ADVISOR: "a",
    -Piece.ELEPHANT: "e",
    -Piece.ROOK: "r",
    -Piece.KNIGHT: "n",
    -Piece.CANNON: "c",
    -Piece.PAWN: "p",
}

def char_of(piece_code: int) -> str:
    return PIECE_CHAR.get(piece_code, "?")
