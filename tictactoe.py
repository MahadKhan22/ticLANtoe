import sys


def main():
    global list
    list = []
    print("input 'f' to forfeit a match, input 'q' for row and column to quit the game\n")
    while True:
        list.append(game())


def interruptHandler():
    xScore = list.count("x")
    oScore = list.count("o")
    print(f"\nfinal score:\nx: {xScore}\no: {oScore}")
    sys.exit()


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
            print("\nERROR: position filled!\ntry again:")
            return False
    else:
        print(("\nERROR: invalid position!\ntry again:"))
        return False


def game():
    global board
    board = [["-"] *3 for i in range(3)]
    showBoard()
    Xmoves = 0
    while True:

        moved = False
        while not moved:
            player = "x"

            if (col:=input("col: ")) == "f" or (row:=input("row: ")) == "f":
                print(f"\n{player} forfeits")
                if player == "x":
                    return "o"
                return "x"
            elif (col=="q" and row=="q"):
                interruptHandler()
            moved = inputMove(col, row, player)

        showBoard()
        if returnVal:=checkWin():
            return(player)
        Xmoves += 1
        if Xmoves == 5:
            print("\ntie!\n")
        

        moved = False
        while not moved:
            player = "o"
            if (col:=input("col: ")) == "f" or (row:=input("row: ")) == "f":
                print(f"\n{player} forfeits")
                if player == "x":
                    return "o"
                return "x"
            elif (col=="q" and row=="q"):
                interruptHandler()
            moved = inputMove(col, row, player)

        showBoard()
        if returnVal:=checkWin():
            print(f"{player} wins!")
            return(player)


if __name__ == "__main__":
    main()
