import sys

def showBoard():
    global board
    for i in range(3):
        for j in range(3):
            print(f"{board[i][j]}",end=" ")
        print()


def checkWin():
    global board
    for i in range(3):
        letter = board[i][0]
        if letter == "x" or letter ==  "o":
            if board[i][1] == letter and board[i][2] == letter:
                print(f"\n{board[i][0]} wins!\n")
                return True
        letter = board[0][i]
        if letter == "x" or letter == "o":
            if board[1][i] == letter and board[2][i] == letter:
                print(f"\n{board[0][i]} wins!\n")
                return True

    letter = board[1][1]
    if letter == "x" or letter == "o":
        if board[0][0] == letter and board[2][2] == letter:
            print(f"\n{board[1][1]} wins!\n")
            return True
        if board[0][2] == letter and board[2][0] == letter:
            print(f"\n{board[1][1]} wins!\n")
            return True
        return False


def inputMove(col, row, player):
    global board
    col,row = int(col)-1, int(row)-1
    if 0<=col<=2 and 0<=row<=2:
        if board[row][col] != "x" and board[row][col] != "o":
            board[row][col] = player
            return True
        else:
            print("\nERROR: position filled!\n")
            return False
    else:
        print(("\nERROR: invalid position!\n"))
        return False


def game():
    global board
    board = [["-"] *3 for i in range(3)]
    Xmoves = 0
    while True:

        moved = False
        while not moved:
            player = "x"
            col = input("col: ")
            row = input("row: ")
            if col == "q" or row == "q":
                print(f"\n{player} forfeits")
                if player == "x":
                    return "o"
                return "x"
            moved = inputMove(col, row, player)

        showBoard()
        if returnVal:=checkWin():
            return(player)
        Xmoves += 1
        if Xmoves == 5:
            sys.exit("\ntie!\n")
        

        moved = False
        while not moved:
            player = "o"
            col = input("col: ")
            row = input("row: ")
            if col == "q" or row == "q":
                print(f"\n{player} forfeits")
                if player == "x":
                    return "o"
                return "x"
            moved = inputMove(col, row, player)

        showBoard()
        if returnVal:=checkWin():
            return(player)


if __name__ == "__main__":
    list = []
    print("input 'q' to forfeit a match, input 'Ctrl+c' to end the game\n")
    while True:
        try:
            list.append(game())
        except KeyboardInterrupt:
            xScore = list.count("x")
            oScore = list.count("o")
            sys.exit(f"\n\nfinal score:\nx: {xScore}\no: {oScore}")