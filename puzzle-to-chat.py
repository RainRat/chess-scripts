#Apache 2.0 license

'''
I was looking at the lichess chess puzzles. They are situations where there is only one correct move. There's over 3 million of them. https://database.lichess.org/#puzzles

They look like:

00sHx,q3k1nr/1pp1nQpp/3p4/1P2p3/4P3/B1PP1b2/B5PP/5K2 b k - 0 17,e8d7 a2e6 d7d8 f7f8,1760,80,83,72,mate mateIn2 middlegame short,https://lichess.org/yyznGmXs/black#34,Italian_Game Italian_Game_Classical_Variation

They could be made into a Q and A format i.e.

User: The situation in a chess game is q3k1nr/1pp1nQpp/3p4/1P2p3/4P3/B1PP1b2/B5PP/5K2 and your opponent plays e8 to d7. What is the only correct move?
Assistant: a2 to e6

There could be more done like reading the position to describe it in prose, using the tags to talk about the position, or filtering to positions that are simpler to understand.

For a start, I only used puzzles that were one move. Future possibilities include conversing over multiple moves, or just using one move from each puzzle regardless.

'''

import pandas as pd
import chess
import random

def board_to_string(board):
    return board.board_fen() if random.choice([True, False]) else str(board)

def process_puzzle_row(row):
    outBuffer='User: '
    # Extract the FEN and moves from the row
    moves = row["Moves"].split()
    if len(moves)>2:
        return None
    fen = row["FEN"]
    themes = row["Themes"].split()
    random.shuffle(themes)
    # Create a chess board from the FEN
    board = chess.Board(fen)
    outBuffer+=random.choice(['I have the following ', 'Imagine this ', 'We are playing a chess game. We reach this '])
    outBuffer+=random.choice(['chess position.', 'position in chess.'])
    outBuffer+='\r\n'
    if random.choice([True, False]): #the puzzle starts at the second move in the list. decide whether to give the first move or start the puzzle immediately
        outBuffer+=board_to_string(board) #give the previous move
        outBuffer+='\r\n'
        outBuffer+=random.choice(['I make the following move: ', 'My move: '])
        outBuffer+= board.san(chess.Move.from_uci(moves[0]))
        board.push(chess.Move.from_uci(moves[0]))
    else:
        board.push(chess.Move.from_uci(moves[0])) #just provide the position
        outBuffer+=board_to_string(board)
    outBuffer+='\r\n'
    if board.turn==chess.WHITE:
        outBuffer+="White"
    else:
        outBuffer+="Black"
    outBuffer+=random.choice(['\'s turn. ', ' to play. '])
    outBuffer=outBuffer+random.choice(['What is your move?', 'Your move.'])
    
    outBuffer=outBuffer+'\r\nAssistant: '
    outBuffer+=random.choice(['My move is ', 'I play '])
    outBuffer+= board.san(chess.Move.from_uci(moves[1]))
    outBuffer+= '.\r\n'

    themeBuffer=''
    for theme in themes:
        if theme=='mateIn1':
            themeBuffer=random.choice(['Checkmate!', 'I win!']) #yes this is replacement, not concatenation. If game is over, no point rambling on.
            break
        elif theme=='mate':
            themeBuffer+=random.choice(['I now have an unstoppable checkmating attack. ', 'Looks like you cannot win now. '])
        elif theme=='hangingPiece':
            themeBuffer+=random.choice(['Looks like that piece is free for the taking. ', 'That piece is mine now. '])
        elif theme=='crushing':
            themeBuffer+=random.choice(['That will give me a crushing advantage. ', 'Looks like I have a major advantage now. '])
        elif theme=='advantage':
            themeBuffer+=random.choice(['That will give me an advantage. ', 'Looks like I have an advantage now. '])
        elif theme=='enPassant':
            themeBuffer+=random.choice(['Ah, en passant. If a pawn moves two spaces through a square an enemy pawn could capture it, then it can be captured as though it were captured "in passing" but only on the very next move. ', 'En passant, nice. '])
        elif theme=='defensiveMove':
            themeBuffer+=random.choice(['A defensive move. ', 'I will defend against your attack. '])
    outBuffer+=themeBuffer.strip()+'\r\n\r\n'
    return(outBuffer)

try:
    df = pd.read_csv("lichess_db_puzzle.csv")
    num_samples = 30
    sampled_df = df.sample(n=num_samples)

    with open('assist.txt', 'w', encoding='utf8') as output:
        for _, row in sampled_df.iterrows():
            puzzle_output = process_puzzle_row(row)
            if puzzle_output is None:
                continue
            output.write(puzzle_output)
            print(puzzle_output)
            print("=" * 50)

except IOError:
    print("Error in reading CSV file or writing to assist.txt")
except pd.errors.EmptyDataError:
    print("Error: The CSV file is empty")
except Exception as e:
    print(f"An error occurred: {e}")

