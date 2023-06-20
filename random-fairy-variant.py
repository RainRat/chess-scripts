import argparse
import random
import os

# parse command-line arguments
parser = argparse.ArgumentParser(description='Generate a random FEN for a chess variant.')
parser.add_argument('--custom_pawn', action='store_true',
                    help='Use a custom pawn (default: False)')
parser.add_argument('--compound_piece', action='store_true',
                    help='Use compound pieces (ie. a Queen is a compound piece because it moves like a knight and a bishop) (default: False)')
parser.add_argument('--hoppel_poppel', action='store_true',
                    help='Enable Hoppel-Poppel mode (each piece captures differently than it attacks) (default: False)')
parser.add_argument('--output_file', type=str, default='random_variant.ini',
                    help='The filename for the output FEN (default: random_variant.ini)')
args = parser.parse_args()

#COMPOUND_PIECE and HOPPEL_MODE at same time is currently too complicated

def generate_random_FEN():

    fen = """
[random-fairy:chess]
extinctionPseudoRoyal = true
king = -
"""
    bag = ['w', 'f', 'd', 'a', 'n', 'h', 'c', 'z', 'g', 'r', 'b']
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
    fen += f' w - - 0 1\n'
    fen += 'extinctionPieceTypes = '+fen_list[3]+'\n'
    fen += 'promotionPieceTypes = '+''.join(fen_list[4:])+'\n'
    for i, item in enumerate(fen_list[:5], 1):
        if args.compound_piece or args.hoppel_poppel:
            bag_copy = bag.copy()
            bag_copy.remove(item)
            second_mode = random.choice(bag_copy)
            if args.compound_piece:
                fen += f'customPiece{i} = {item}:{item.upper()}{second_mode.upper()}\n'
            else:
                fen += f'customPiece{i} = {item}:m{item.upper()}c{second_mode.upper()}\n'
        else:
            fen += f'customPiece{i} = {item}:{item.upper()}\n'
    if args.custom_pawn:
        pawnModes = random.sample(bag[:-6], 2) #pawns that jump 3 or more squares probably too strong.
        fen += 'pawn = -\n'
        fen += 'pawnTypes = p\n'
        fen += 'enPassantTypes = -\n' #calculating en passant for some too complicated
        fen += f'customPiece6 = p:mf{pawnModes[0].upper()}cf{pawnModes[1].upper()}\n'
    return fen

# Write the FEN to a file
with open(args.output_file, 'w') as f:
    random_fen=generate_random_FEN()
    f.write(random_fen)
    print(random_fen)
