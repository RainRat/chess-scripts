import argparse
import random

PIECE_BAG = ['w', 'f', 'd', 'a', 'n', 'h', 'c', 'z', 'g', 'r', 'b']
BASE_FEN_STRUCTURE = """
[random-fairy:chess]
extinctionPseudoRoyal = true
king = -
"""

parser = argparse.ArgumentParser(description='Generate a random Fairy Stockfish .ini for a chess variant.')
parser.add_argument('--custom_pawn', action='store_true',
                    help='Use a custom pawn (default: False)')
parser.add_argument('--compound_piece', action='store_true',
                    help='Use compound pieces (ie. a Queen is a compound piece because it moves like a rook and a bishop) (default: False)')
parser.add_argument('--hoppel_poppel', action='store_true',
                    help='Enable Hoppel-Poppel mode (each piece captures differently than it attacks) (default: False)')
parser.add_argument('--output_file', type=str, default='random_variant.ini',
                    help='The filename for the output FEN (default: random_variant.ini)')
args = parser.parse_args()

if args.compound_piece and args.hoppel_poppel:
    raise ValueError("Error: Cannot enable both compound_piece and hoppel_poppel at the same time.")

def generate_piece_fen(PIECE_BAG, compound_piece, hoppel_poppel):
    """
    Generates a FEN string for the custom pieces.
    """
    pieces = random.sample(PIECE_BAG, 5)
    fen_list = pieces[:5] + pieces[2::-1]
    fen = ''
    for i, item in enumerate(fen_list[:5], 1):
        if compound_piece or hoppel_poppel:
            bag_copy = PIECE_BAG.copy()
            bag_copy.remove(item)
            second_mode = random.choice(bag_copy)
            if compound_piece:
                fen += f'customPiece{i} = {item}:{item.upper()}{second_mode.upper()}\n'
            else:
                fen += f'customPiece{i} = {item}:m{item.upper()}c{second_mode.upper()}\n'
        else:
            fen += f'customPiece{i} = {item}:{item.upper()}\n'

    return fen, fen_list

def generate_pawn_fen(PIECE_BAG):
    """
    Generates a FEN string for the custom pawn.
    """
    pawnModes = random.sample(PIECE_BAG[:-6], 2)  # pawns that jump 3 or more squares probably too strong.
    fen = 'pawn = -\n'
    fen += 'pawnTypes = p\n'
    fen += 'enPassantTypes = -\n'  # calculating en passant for some too complicated
    fen += f'customPiece6 = p:mf{pawnModes[0].upper()}cf{pawnModes[1].upper()}\n'
    return fen

def generate_random_FEN(compound_piece, hoppel_poppel, custom_pawn):
    """
    Generates a random FEN string based on the given conditions.
    """
    #Does not contain all atoms. L and C are same. J and Z are same.
    fen = BASE_FEN_STRUCTURE
    piece_fen, fen_list = generate_piece_fen(PIECE_BAG, compound_piece, hoppel_poppel)
    fen += piece_fen
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
    fen += ' w - - 0 1\n'
    fen += 'extinctionPieceTypes = '+fen_list[3]+'\n'
    fen += 'promotionPieceTypes = '+''.join(fen_list[4:])+'\n'
    if custom_pawn:
        fen += generate_pawn_fen(PIECE_BAG)
    return fen

try:
    random_fen = generate_random_FEN(args.compound_piece, args.hoppel_poppel, args.custom_pawn)
    print(random_fen)
    with open(args.output_file, 'w') as f:
        f.write(random_fen)
except Exception as e:
    print(f"Error occurred: {e}")
