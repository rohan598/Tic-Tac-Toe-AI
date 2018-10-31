from statistics import mean
from timeit import default_timer as timer
import random
import copy

STATEO = 3
STATEX = 5
def setup_tic_tac_toe(c=0):
    grid = [[2, 2, 2, 2],
            [2, 2, 2, 2],
            [2, 2, 2, 2],
            [2, 2, 2, 2]]
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
        itr = random.randint(0, 15)
        if grid[c_moves[itr][0]][c_moves[itr][1]] == 2:
            grid[c_moves[itr][0]][c_moves[itr][1]] = move
            break
    return grid

def ctv_converter(score):
    for i in range(10):
        if score[0][i] == 4:
            score[0][i] == 1000
        elif score[0][i] == 3:
            score[0][i] = 100
        elif score[0][i] == 2:
            score[0][i] = 10
        elif score[0][i] == 1:
            score[0][i] = 1
        else:
            score[0][i] = 0
        if score[0][i] == 4:
            score[0][i] == -1000
        elif score[1][i] == 3:
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
    for i in range(16):
        if grid[int(i / 4)][i % 4] == 2:
            grid[int(i / 4)][i % 4] = move
            count = count + 1
            t = copy.deepcopy(grid)
            t_config.append(t)
            grid[int(i / 4)][i % 4] = 2
    return t_config

def heuristic(grid):
    final_score = 0
    score = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    for x in range(4):
        for y in range(4):
            if grid[x][y] == 5:
                score[0][x] = score[0][x] + 1
            elif grid[x][y] == 3:
                score[1][x] = score[1][x] + 1
        if score[0][x] != 0 and score[1][x] != 0:
            score[0][x], score[1][x] = (0,0)

    for y in range(4):
        for x in range(4):
            if grid[x][y] == 5:
                score[0][y + 4] = score[0][y + 4] + 1
            elif grid[x][y] == 3:
                score[1][y + 4] = score[1][y + 4] + 1
        if score[0][y + 4] != 0 and score[1][y + 4] != 0:
            score[0][y + 4], score[1][y + 4] = (0,0)
    j = 3
    for i in range(4):
        if grid[i][i] == 5:
            score[0][8] = score[0][8] + 1
        elif grid[i][i] == 3:
            score[1][8] = score[1][8] + 1
        if grid[i][j] == 5:
            score[0][9] = score[0][9] + 1
        elif grid[i][j] == 3:
            score[1][9] = score[1][9] + 1
        j = j - 1
    if score[0][8] != 0 and score[1][8] != 0:
            score[0][8], score[1][8] = (0,0)
    if score[0][9] != 0 and score[1][9] != 0:
        score[0][9], score[1][9] = (0, 0)
    score = ctv_converter(score)
    for i in range(10):
        final_score = final_score + score[0][i] + score[1][i]
    return final_score

def minimax_wrapper(grid, move, level, itr, count, computer):
    if level > itr and count < 16:
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
    c1 = grid[0][0] * grid[1][0] * grid[2][0] * grid[3][0]
    c2 = grid[0][1] * grid[1][1] * grid[2][1] * grid[3][1]
    c3 = grid[0][2] * grid[1][2] * grid[2][2] * grid[3][2]
    c4 = grid[0][3] * grid[1][3] * grid[2][3] * grid[3][3]
    r1 = grid[0][0] * grid[0][1] * grid[0][2] * grid[0][3]
    r2 = grid[1][0] * grid[1][1] * grid[1][2] * grid[1][3]
    r3 = grid[2][0] * grid[2][1] * grid[2][2] * grid[2][3]
    r4 = grid[3][0] * grid[3][1] * grid[3][2] * grid[3][3]
    d1 = grid[0][0] * grid[1][1] * grid[2][2] * grid[3][3]
    d2 = grid[0][3] * grid[1][2] * grid[2][1] * grid[3][0]
    if move == STATEX:
        if c1 == 625 or c2 == 625 or c3 == 625 or c4 == 625 or r1 == 625 or r2 == 625 or r3 == 625 or r4 == 625 or d1 == 625 or d2 == 625:
            return 1
    else:
        if c1 == 81 or c2 == 81 or c3 == 81 or c4 == 81 or r1 == 81 or r2 == 81 or r3 == 81 or r4 == 81 or d1 == 81 or d2 == 81:
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
    elif count == 16:
        over = 2
    return (grid, move, count, over)

def auto_play():
    computer_ai, computer_random = STATEO,STATEX
    grid, move, count = setup_tic_tac_toe(2)
    c_moves = [[1, 1], [1, 2], [2, 1], [2, 2],
               [0, 0], [3, 3], [0, 3], [3, 0],
               [0, 1], [0, 2], [3, 1], [3, 2],
               [1, 0], [2, 0], [1, 3], [2, 3]]
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
            if count == 15:
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
#print("count_wins: ", count_wins, "count_loses: ", count_loses, "count_draws: ", count_draws, sep='\n')
