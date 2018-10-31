from ttt_helper import toss, setup_tic_tac_toe, STATEX, STATEO, print_wrapper, computer_move, computer_random_move, minimax_wrapper, update
from statistics import mean
from timeit import default_timer as timer

# auto-play for statistical analysis
def auto_play():
    # toss to choose player 1
    computer_ai, computer_random = STATEO,STATEX

    # set up tic tac toe board
    grid, move, count = setup_tic_tac_toe(2)
    c_moves = [[1, 1], [0, 0], [0, 2], [2, 0], [2, 2],
               [0, 1], [1, 0], [1, 2], [2, 1]]

    # game play
    # first human and computer move
    if computer_ai == STATEX:
        print("Computer AI Bot Chance")
        grid[1][1] = STATEX
        print_wrapper(grid)
        print("Computer Random Bot Chance")
        grid = computer_random_move(grid, c_moves, STATEO)
    else:
        print("Computer Random Bot Chance")
        grid = computer_random_move(grid, c_moves, STATEX)
        print_wrapper(grid)
        print("Computer AI Bot Chance")
        grid = computer_move(grid, c_moves, STATEO)
    print_wrapper(grid)

    # following moves, 1 level look-ahead
    while True:
        # human plays
        if computer_random == move:
            print("Computer Random Bot Chance")
            grid = computer_random_move(grid, c_moves, move)

        # computer plays
        else:
            print("Computer AI Bot Chance")
            if count == 8:
                grid = computer_move(grid, c_moves, move)
            else:
                grid = minimax_wrapper(grid, computer_ai, 4, 0, count + 1, computer_ai)

        # update
        grid, move, count, over = update(grid, move, count, computer_ai, computer_random)
        if over:
            return over

def auto_play_wrapper(epoch=100,n_epoch=1):
    count_wins = []
    count_loses = []
    count_draws = []
    time_avg = []
    start = timer()
    for i in range(n_epoch):
        count_win = 0
        count_lose = 0
        count_draw = 0
        for j in range(epoch):
            x = auto_play()
            if x == 1:
                count_win += 1
            elif x == -1:
                count_lose +=1
            else:
                count_draw +=1
        count_wins.append(count_win)
        count_loses.append(count_lose)
        count_draws.append(count_draw)
    end = timer()
    time_avg.append(end-start)
    return (count_wins,count_loses,count_draws,time_avg)


(count_wins, count_loses, count_draws,time_avg) = auto_play_wrapper(epoch=100, n_epoch=10)
print("count_wins average: ", mean(count_wins), "count_draws average: ", mean(count_draws), "count_loses average: ", mean(count_loses), "time average: ", mean(time_avg), sep='\n')
# print("count_wins: ", count_wins, "count_loses: ", count_loses, "count_draws: ", count_draws, sep='\n')