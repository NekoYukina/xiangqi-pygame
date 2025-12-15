from __future__ import annotations
import random

from core.board import Board
from core.const import Side
from core.movegen import gen_legal_moves

def main():
    b = Board.initial()
    print(b.pretty())

    side = b.side_to_move
    moves = gen_legal_moves(b, side)
    print(f"Legal moves for {side.name}: {len(moves)}")

    if moves:
        mv = random.choice(moves)
        print("Play:", mv)
        b.make_move(mv)
        print(b.pretty())

if __name__ == "__main__":
    main()
