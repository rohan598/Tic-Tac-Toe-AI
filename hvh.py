from ttt_helper import  setup_tic_tac_toe, STATEO, STATEX, print_wrapper, win

# testing game mode human vs human version
def play_hvh():
    # set up tic tac toe board
    grid, move, count = setup_tic_tac_toe()

    while True:
        if move == STATEX:
            print("Player 1 move ")
        else:
            print("Player 2 move ")

        while True:
            place = int(input())
            if place == 10:
                win_condition = 2
            elif grid[int(place / 3)][place % 3] == 2:
                grid[int(place / 3)][place % 3] = move
                break
            else:
                print("illegal move, choose another position")

        # modify
        if win_condition != 2:
            win_condition = win(grid, move)
            count = count + 1
            if move == STATEX:
                move = STATEO
            else:
                move = STATEX

        # print board
        print_wrapper(grid)

        if win_condition == 1:
            print("Player 1 won")
            break
        elif win_condition == -1:
            print("Player 2 won")
            break
        elif win_condition == 2 or count == 9:
            print("Match Drawn")
            break
