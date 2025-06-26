
gameBord = [["","",""],["","",""],["","",""]]
players = {"player1": "ema","player2": "maki"}
print(len(gameBord))
def add(x,y,symbol):
        for i in range(len(gameBord)):
            for j in range(len(gameBord)):
                if i == x and j == y:
                 gameBord[x][y] = symbol
                #  print(gameBord[x][y])

def renderGameBoard():
    for i in range(len(gameBord)):
            row = ""
            for j in range(len(gameBord)):
                row += (f" {gameBord[i][j]} | ")
            print(row)
            print(" ------------")
def checkOX(symbol):
    if(symbol == 'x' or symbol == 'o' and symbol != ''):
        return False
    else:
        return True

def checkInputs(symbol):
    if(symbol == '0' or symbol == '1' or symbol == '2' and symbol != ''):
        return False
    else:
        return True
# def check_the_winner():
def takeInputs():
    i = 1
    turn = 0
    print("   Play tic tac toe ")
    player1 = input("player 1 turn x /o ")
    while(checkOX(player1)):
        player1 = (input("symbol must be O / X : "))
    player2 = 'o' if player1 == 'x' else 'x'

    print(player1)
    print(player2)
    while i < 9:
        if turn % 2 == 0:
            player1_posx = (input("player 1 position x : "))
            while(checkInputs(player1_posx)):
                player1_posx = (input("number must be between 0 and 2 : "))

            player1_posy = (input("player 1 position y : "))
            while(checkInputs(player1_posy)):
                player1_posy = (input("number must be between 0 and 2 : "))

            # print(f"x {player1_posx} : y {player1_posy}")
            add(int(player1_posx),int(player1_posy),player1)
            renderGameBoard()
        else:
            player2_posx = (input("player 2 position x : "))
            while(checkInputs(player2_posx)):
                player2_posx = (input("number must be between 0 and 2 : "))

            player2_posy = (input("player 2 position y : "))
            while(checkInputs(player2_posy)):
                player2_posy = (input("number must be between 0 and 2 : "))

            add(int(player2_posx),int(player2_posy),player2)
            renderGameBoard()
        turn += 1


takeInputs()





