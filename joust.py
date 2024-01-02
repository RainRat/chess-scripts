#Generate .ini file for Joust starting positions for Fairy Stockfish. One Knight is placed on each player's home row.
#Most players randomize the position on the starting row for more varied games. Generate a .ini file with all 64 start positions,
#so only one number has to be picked.
counter=1

with open('joust.ini', 'w') as f:
    for i in range(8):
        for j in range(8):
            f.write(f'[joust{counter}:joust]\n')
            knight_pos1 = str(i) if i != 0 else ""
            opposite_knight_pos1 = str(7-i) if 7-i != 0 else ""
            knight_pos2 = str(j) if j != 0 else ""
            opposite_knight_pos2 = str(7-j) if 7-j != 0 else ""
            f.write(f"startFen = {knight_pos1}n{opposite_knight_pos1}/8/8/8/8/8/8/{knight_pos2}N{opposite_knight_pos2}\n")
            counter += 1
