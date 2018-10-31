from ttt_helper import  toss, setup_tic_tac_toe, STATEX, STATEO, print_wrapper, computer_move, human_move, minimax_wrapper, update
# defend itself, one level lookahead
def play_ai(level):
    # toss to choose player 1
    computer, human = toss()

    # set up tic tac toe board
    grid, move, count = setup_tic_tac_toe(2)
    c_moves = [[1, 1], [0, 0], [0, 2], [2, 0], [2, 2],
               [0, 1], [1, 0], [1, 2], [2, 1]]

    # game play
    # first human and computer move
    if computer == STATEX:
        print("Computer's Chance")
        grid[1][1] = STATEX
        print_wrapper(grid)
        grid = human_move(grid, STATEO)
    else:
        grid = human_move(grid, STATEX)
        print_wrapper(grid)
        print("Computer's Chance")
        grid = computer_move(grid, c_moves, STATEO)
    print_wrapper(grid)

    # following moves, 1 level look-ahead
    while True:
        # human plays
        if human == move:
            grid = human_move(grid, move)

        # computer plays
        else:
            print("Computer's Chance")
            if count == 8:
                grid = computer_move(grid, c_moves, move)
            else:
                grid = minimax_wrapper(grid, computer, level, 0, count+1, computer)

        # update
        grid, move, count, over = update(grid, move, count, computer, human)
        if over:
            break

