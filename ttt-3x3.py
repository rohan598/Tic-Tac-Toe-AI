from statistics import mean
from timeit import default_timer as timer
import random
import copy

STATEO = 3
STATEX = 5
def setup_tic_tac_toe(c=0):
    grid = [[2, 2, 2],
            [2, 2, 2],
            [2, 2, 2]]
    move = STATEX
    count = c
    return (grid, move, count)

def computer_move(grid, c_moves, move):
    itr = 0
    while True:
        if grid[c_moves[itr][0]][c_moves[itr][1]] == 2:
            grid[c_moves[itr][0]][c_moves[itr][1]] = move
            break
        itr = itr + 1
    return grid

def computer_random_move(grid, c_moves, move):
    while True:
        itr = random.randint(0, 8)
        if grid[c_moves[itr][0]][c_moves[itr][1]] == 2:
            grid[c_moves[itr][0]][c_moves[itr][1]] = move
            break
    return grid

def ctv_converter(score):
    for i in range(8):
        if score[0][i] == 3:
            score[0][i] = 100
        elif score[0][i] == 2:
            score[0][i] = 10
        elif score[0][i] == 1:
            score[0][i] = 1
        else:
            score[0][i] = 0
        if score[1][i] == 3:
            score[1][i] = -100
        elif score[1][i] == 2:
            score[1][i] = -10
        elif score[1][i] == 1:
            score[1][i] = -1
        else:
            score[1][i] = 0
    return score

def generateCon(grid, move):
    t_config = []
    count = -1
    for i in range(9):
        if grid[int(i / 3)][i % 3] == 2:
            grid[int(i / 3)][i % 3] = move
            count = count + 1
            t = copy.deepcopy(grid)
            t_config.append(t)
            grid[int(i / 3)][i % 3] = 2
    return t_config

def heuristic(grid):
    final_score = 0
    score = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    for x in range(3):
        for y in range(3):
            if grid[x][y] == 5:
                score[0][x] = score[0][x] + 1
            elif grid[x][y] == 3:
                score[1][x] = score[1][x] + 1
        if score[0][x] != 0 and score[1][x] != 0:
            score[0][x], score[1][x] = (0,0)

    for y in range(3):
        for x in range(3):
            if grid[x][y] == 5:
                score[0][y + 3] = score[0][y + 3] + 1
            elif grid[x][y] == 3:
                score[1][y + 3] = score[1][y + 3] + 1
        if score[0][y + 3] != 0 and score[1][y + 3] != 0:
            score[0][y + 3], score[1][y + 3] = (0,0)
    j = 2
    for i in range(3):
        if grid[i][i] == 5:
            score[0][6] = score[0][6] + 1
        elif grid[i][i] == 3:
            score[1][6] = score[1][6] + 1
        if grid[i][j] == 5:
            score[0][7] = score[0][7] + 1
        elif grid[i][j] == 3:
            score[1][7] = score[1][7] + 1
        j = j - 1
    if score[0][6] != 0 and score[1][6] != 0:
            score[0][6], score[1][6] = (0,0)
    if score[0][7] != 0 and score[1][7] != 0:
        score[0][7], score[1][7] = (0, 0)
    score = ctv_converter(score)
    for i in range(8):
        final_score = final_score + score[0][i] + score[1][i]
    return final_score

def minimax_wrapper(grid, move, level, itr, count, computer):
    if level > itr and count < 9:
        t_config = generateCon(grid, move)
        f_config = t_config
        f_config = []
        if move == STATEX:
            move = STATEO
        else:
            move = STATEX
        for i in range(len(t_config)):
            f_config.append(minimax_wrapper(t_config[i], move, level, itr + 1, count+1, computer))
        if move == STATEX:
            move = STATEO
        else:
            move = STATEX
        score = []
        for i in range(0, len(f_config)):
            score.append(heuristic(f_config[i]))
        max_index = -1
        min_index = -1
        if move == STATEX:
            max_val = -10000
            for i in range(len(f_config)):
                if max_val < score[i]:
                    max_val = score[i]
                    max_index = i
        else:
            min_val = 10000
            for i in range(len(f_config)):
                if min_val > score[i]:
                    min_val = score[i]
                    min_index = i
        if min_index != -1:
            grid = t_config[min_index]
        else:
            grid = t_config[max_index]
    return grid

def win(grid, move):
    c1 = grid[0][0] * grid[1][0] * grid[2][0]
    c2 = grid[0][1] * grid[1][1] * grid[2][1]
    c3 = grid[0][2] * grid[1][2] * grid[2][2]
    r1 = grid[0][0] * grid[0][1] * grid[0][2]
    r2 = grid[1][0] * grid[1][1] * grid[1][2]
    r3 = grid[2][0] * grid[2][1] * grid[2][2]
    d1 = grid[0][0] * grid[1][1] * grid[2][2]
    d2 = grid[2][0] * grid[1][1] * grid[0][2]
    if move == STATEX:
        if c1 == 125 or c2 == 125 or c3 == 125 or r1 == 125 or r2 == 125 or r3 == 125 or d1 == 125 or d2 == 125:
            return 1
    else:
        if c1 == 27 or c2 == 27 or c3 == 27 or r1 == 27 or r2 == 27 or r3 == 27 or d1 == 27 or d2 == 27:
            return -1
    return 0

def update(grid, move, count, computer, human):
    win_condition = win(grid, move)
    count = count + 1
    if move == STATEX:
        move = STATEO
    else:
        move = STATEX
    over = 0
    if (win_condition == 1 and computer == STATEX) or (win_condition == -1 and computer == STATEO):
        over = 1
    elif (win_condition == 1 and human == STATEX) or (win_condition == -1 and human == STATEO):
        over = -1
    elif count == 9:
        over = 2
    return (grid, move, count, over)

def auto_play():
    computer_ai, computer_random = STATEO,STATEX
    grid, move, count = setup_tic_tac_toe(2)
    c_moves = [[1, 1], [0, 0], [0, 2], [2, 0], [2, 2],
               [0, 1], [1, 0], [1, 2], [2, 1]]
    if computer_ai == STATEX:
        grid[1][1] = STATEX
        grid = computer_random_move(grid, c_moves, STATEO)
    else:
        grid = computer_random_move(grid, c_moves, STATEX)
        grid = computer_move(grid, c_moves, STATEO)
    while True:
        if computer_random == move:
            grid = computer_random_move(grid, c_moves, move)
        else:
            if count == 8:
                grid = computer_move(grid, c_moves, move)
            else:
                grid = minimax_wrapper(grid, computer_ai, 4, 0, count + 1, computer_ai)
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