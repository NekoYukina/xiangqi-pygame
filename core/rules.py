from __future__ import annotations
from .board import Board
from .const import Side

def is_face_to_face(board: Board) -> bool:
    """将帅照面：同列无遮挡则为 True（非法/将军的一部分）。占位实现后面补。"""
    # TODO: 找红帅/黑将位置，若同列且中间无子 -> True
    return False

def in_check(board: Board, side: Side) -> bool:
    """side 方是否被将军。占位：后续实现（含照面）。"""
    # TODO: 需要对方的攻击走法判断（可用 movegen 的攻击判定或专用函数）
    return False

def is_checkmate(board: Board, side: Side, legal_moves_provider) -> bool:
    """side 方是否将死：被将军且无合法走法"""
    if not in_check(board, side):
        return False
    return len(legal_moves_provider(board, side)) == 0
