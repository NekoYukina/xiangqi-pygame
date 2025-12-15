from __future__ import annotations
from typing import List

from .board import Board
from .move import Move
from .const import Side, Piece, type_of, side_of, i_to_rc, rc_to_i, BOARD_ROWS, BOARD_COLS
from . import rules

def gen_pseudo_legal_moves(board: Board, side: Side) -> List[Move]:
    moves: List[Move] = []
    for pos, p in board.iter_pieces(side):
        t = type_of(p)
        if t == Piece.ROOK:
            moves.extend(_gen_rook(board, pos, side))
        elif t == Piece.KNIGHT:
            moves.extend(_gen_knight(board, pos, side))
        elif t == Piece.CANNON:
            moves.extend(_gen_cannon(board, pos, side))
        elif t == Piece.PAWN:
            moves.extend(_gen_pawn(board, pos, side))
        elif t == Piece.KING:
            moves.extend(_gen_king(board, pos, side))
        elif t == Piece.ADVISOR:
            moves.extend(_gen_advisor(board, pos, side))
        elif t == Piece.ELEPHANT:
            moves.extend(_gen_elephant(board, pos, side))
    return moves

def gen_legal_moves(board: Board, side: Side) -> List[Move]:
    """伪合法 -> 合法（过滤走后自家仍被将军/照面）"""
    legal: List[Move] = []
    for mv in gen_pseudo_legal_moves(board, side):
        board.make_move(mv)
        # 走后轮到对方，但我们要检查"原side是否被将军"
        if (not rules.in_check(board, side)) and (not rules.is_face_to_face(board)):
            legal.append(mv)
        board.undo_move()
    return legal

def _in_bounds(r: int, c: int) -> bool:
    return 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS

def _try_add(board: Board, side: Side, frm: int, to: int, moves: List[Move]) -> None:
    target = board.piece_at(to)
    if target == 0:
        moves.append(Move(frm, to))
    else:
        if side_of(target) != side:
            moves.append(Move(frm, to, captured=target))

def _gen_rook(board: Board, pos: int, side: Side) -> List[Move]:
    moves: List[Move] = []
    r, c = i_to_rc(pos)
    # 四个方向直线
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        rr, cc = r + dr, c + dc
        while _in_bounds(rr, cc):
            to = rc_to_i(rr, cc)
            target = board.piece_at(to)
            if target == 0:
                moves.append(Move(pos, to))
            else:
                if side_of(target) != side:
                    moves.append(Move(pos, to, captured=target))
                break
            rr += dr
            cc += dc
    return moves

def _gen_knight(board: Board, pos: int, side: Side) -> List[Move]:
    # TODO: 马走日 + 蹩马腿
    # 提示：先定义8个(leg, to)组合：腿被占则该方向全废
    return []

def _gen_cannon(board: Board, pos: int, side: Side) -> List[Move]:
    # TODO: 炮平移像车；吃子需要隔一个"炮架"
    return []

def _gen_pawn(board: Board, pos: int, side: Side) -> List[Move]:
    # TODO: 兵/卒：未过河只能前，过河可左右，不能后退
    return []

def _gen_king(board: Board, pos: int, side: Side) -> List[Move]:
    # TODO: 将/帅：九宫内一步；并考虑照面（可在 rules 里统一过滤）
    return []

def _gen_advisor(board: Board, pos: int, side: Side) -> List[Move]:
    # TODO: 士/仕：九宫内斜一步
    return []

def _gen_elephant(board: Board, pos: int, side: Side) -> List[Move]:
    # TODO: 象/相：田字，塞象眼，不能过河
    return []
