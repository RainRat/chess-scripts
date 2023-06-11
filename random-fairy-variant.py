import random
import os

CUSTOM_PAWN=True
COMPOUND_PIECE=False
HOPPEL_POPPEL_MODE=True #COMPOUND_PIECE and HOPPEL_MODE at same time is currently too complicated

def generate_random_FEN():

    fen = """
[random-fairy:chess]
extinctionPseudoRoyal = true
king = -
"""
    bag = ['w', 'f', 'd', 'a', 'h', 'c', 'z', 'g', 'n', 'r', 'b']
    #Does not contain all atoms. L and C are same. J and Z are same.
    pieces = random.sample(bag, 5)
    fen_list = pieces[:5] + pieces[2::-1]

    # Assemble the full FEN string for both sides
    fen += 'startFen = ' + '/'.join([
        ''.join(fen_list).lower(),
        'pppppppp',
        '8',
        '8',
        '8',
        '8',
        'PPPPPPPP',
        ''.join(fen_list).upper()
    ])

    # Add the rest of the FEN string
    fen += f' w - - 0 1\r\n'
    fen += 'extinctionPieceTypes = '+fen_list[3]+'\r\n'
    for i, item in enumerate(fen_list[:5], 1):
        if COMPOUND_PIECE or HOPPEL_POPPEL_MODE:
            bag_copy = bag.copy()
            bag_copy.remove(item)
            second_mode = random.choice(bag_copy)
            if COMPOUND_PIECE:
                fen += f'customPiece{i} = {item}:{item.upper()}{second_mode.upper()}\r\n'
            else:
                fen += f'customPiece{i} = {item}:m{item.upper()}c{second_mode.upper()}\r\n'
        else:
            fen += f'customPiece{i} = {item}:{item.upper()}\n'
    if CUSTOM_PAWN:
        pawnModes = random.sample(bag[:-2], 2) #pawnRooks and pawnBishops too strong
        fen += 'pawn = -\r\n'
        fen += 'pawnTypes = p\r\n'
        fen += 'enPassantTypes = -\r\n' #calculating en passant for some too complicated
        fen += f'customPiece6 = p:mf{pawnModes[0].upper()}cf{pawnModes[1].upper()}\r\n'
    return fen

# Write the FEN to a file
with open('random_variant.ini', 'w') as f:
    random_fen=generate_random_FEN()
    f.write(random_fen)
    print(random_fen)
