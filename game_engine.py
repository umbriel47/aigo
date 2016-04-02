#-*-coding: utf-8-*-
#

import os
import game
import player
# welcome page 

# select mode
while True:
    os.system('clear')
    print '1.\tHuman vs Human'
    print '2.\tHuman(B) vs Com(W)'
    print '3.\tCom(B) vs Human(W)'
    inp = raw_input('Please select mode: ')
    if inp not in ['1', '2', '3']:
        break

    # choose the board size:
    size_lst = (9, 11, 13, 15, 17, 19)
    os.system('clear')
    print '1.\t9  by  9'
    print '2.\t11 by 11'
    print '3.\t13 by 13'
    print '4.\t15 by 15'
    print '5.\t17 by 17'
    print '6.\t19 by 19'
    size = int(raw_input('Please select size: '))
    
    if size not in range(1, 7):
        break
    size = size_lst[size - 1]

    # initialize the game
    symbol1 = u'\u25cf'
    symbol2 = u'\u25cb'
    if inp == '1':
        player1 = player.Player(symbol1)
        player2 = player.Player(symbol2)
    elif inp == '4':
        method1 = 'test'
        method2 = 'test'
        player1 = computer.Computer(symbol1, method1)
        player2 = computer.Computer(symbol2, method2)
    else:
        os.system('clear')
        # TODO: select method
        method = 'test'
        if inp == '2':
            player1 = player.Player(symbol1)
            player2 = computer.Computer(symbol2, method)
        elif inp == '3':
            player1 = computer.Computer(symbol1, method)
            player2 = player.Player(symbol)

    current_game = game.Game(size, (player1, player2))
    current_game.start()


