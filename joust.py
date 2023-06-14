counter=1
with open('joust.ini', 'w') as f:
    for i in range(8):
        for j in range(8):
            f.write('[joust'+str(counter)+':joust]\n')
            number1 = str(i) if i != 0 else ""
            number2 = str(7-i) if 7-i != 0 else ""
            number3 = str(j) if j != 0 else ""
            number4 = str(7-j) if 7-j != 0 else ""
            f.write("startFen = "+ number1 + "n" + number2 + "/8/8/8/8/8/8/" + number3 + "N" + number4 + "\n")
            counter += 1
