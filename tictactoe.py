import sys
import re

def main():
    global list
    list = []
    print("\nmade by MahadKhan22 and BaihusReal")
    print("- inputs: <column> SPACE <row>, eg: '2 3'")
    print("- input 'f f' to forfeit a match.")
    print("have fun! :D\n")

    ans = True
    while ans:
        list.append(game())
        ans = cont()
    discontinue()


def cont():
    cont = input("continue? (y/n): ")
    if cont.strip() == "y":
        return True
    elif cont.strip() == "n":
        return False
    return cont()

def discontinue():
    xScore = list.count("x")
    oScore = list.count("o")
    print(f"final score:\nx: {xScore}\no: {oScore}\n")
    sys.exit()


def showBoard():
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
                print(f"{letter} wins!\n")
                return True
            
        letter = board[0][i]
        if letter == "x" or letter == "o":
            if board[1][i] == letter and board[2][i] == letter:
                print(f"{letter} wins!\n")
                return True

    letter = board[1][1]
    if letter == "x" or letter == "o":
        if board[0][0] == letter and board[2][2] == letter:
            print(f"{letter} wins!\n")
            return True

        if board[0][2] == letter and board[2][0] == letter:
            print(f"{letter} wins!\n")
            return True

        return False


def inputValidate():
    inp = input("\ncolumn & row: ").strip()
    pattern = r"^(?P<column>[1-3]|f) (?P<row>[1-3]|f)$"
    if (matches:=re.search(pattern, inp)):
        col = matches.group("column")
        row = matches.group("row")
        try:
            col, row = int(col)-1, int(row)-1
            return [col, row]
        except:
            if col == "f" or row == "f":
                return "f"
        
    else:
        return False


def inputMove(player):
    global board

    move = inputValidate()
    if not move:
        print(("\nposition invalid!\ntry again:"))
        showBoard()
        return(inputMove(player))
    elif move == "f":
        print(f"\n{player} forfeits")
        if player == "x":
            return "o"
        return "x"   
    else:
        col, row = move[0], move[1]
        if board[row][col] != "-":
            print("\nposition filled!\ntry again:")
            showBoard()
            return(inputMove(player))
        else:
            board[row][col] = player
            return True


def game():
    global board
    board = [["-"] *3 for i in range(3)]
    print("new game: ")
    showBoard()
    Xmoves = 0
    while True:

        if (move:=inputMove("x")) == True:
            pass
        else:
            print("o wins by forfeit!\n")
            return move

        showBoard()
        if checkWin():
            return "x"
        
        Xmoves += 1
        if Xmoves == 5:
            print("\ntie!\n")
            return
    
        if (move:=inputMove("o")) == True:
            pass
        else:
            print("x wins by forfeit!\n")
            return move

        showBoard()
        if checkWin():
            return "o"


if __name__ == "__main__":
    main()
