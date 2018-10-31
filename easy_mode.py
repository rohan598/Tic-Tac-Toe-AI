from ttt_helper import  toss, setup_tic_tac_toe, human_move, computer_random_move, update
# not ai, random moves
def play_easy():
    # toss to choose player 1
    computer, human = toss()

    # set up tic tac toe board
    grid, move, count = setup_tic_tac_toe()
    c_moves = [[1, 1], [0, 0], [0, 2], [2, 0], [2, 2],
               [0, 1], [1, 0], [1, 2], [2, 1]]

    # game play
    while True:
        # Human moves
        if human == move:
            grid = human_move(grid, move)

        # Computer moves
        else:
            grid = computer_random_move(grid, c_moves, move)

        # update
        grid, move, count, over = update(grid, move, count, computer, human)
        if over:
            break
