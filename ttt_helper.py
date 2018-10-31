import random
import copy

STATEO = 3
STATEX = 5

# initializes tic tac toe grid/board
def setup_tic_tac_toe(c=0):
    grid = [[2, 2, 2],
            [2, 2, 2],
            [2, 2, 2]]
    move = STATEX
    count = c
    visual = board_visualizer(grid)
    print_board(visual)
    return (grid, move, count)


# prints tic tac toe board
def print_board(grid):
    print("""      
                |    |
              {} | {}  | {}
            ____|____|____
                |    |
              {} | {}  | {}
            ____|____|____
                |    |
              {} | {}  | {} 
                |    |
    """.format(grid[0][0], grid[0][1], grid[0][2],
               grid[1][0], grid[1][1], grid[1][2],
               grid[2][0], grid[2][1], grid[2][2]))


# converts numbers to X and O
def board_visualizer(grid):
    visual = [[], [], []]
    for x in range(3):
        for y in range(3):
            if grid[x][y] == 5:
                visual[x].append('X')
            elif grid[x][y] == 3:
                visual[x].append('O')
            else:
                visual[x].append(' ')
    return visual

# wrapper for visualizing tic tac toe
def print_wrapper(grid):
    visual = board_visualizer(grid)
    print_board(visual)

# view tic tac toe board before starting the game
def view_board_positions():
    grid = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    print_board(grid)


# toss function to decide x
def toss():
    print("""
        coin toss to start the game first
        h - heads
        t- tails
    """)
    while True:
        coin = input()
        if coin == 'h':
            v = 5
            break
        elif coin == 't':
            v = 0
            break
        else:
            print("invalid choice, enter again!")
    tsum = 0
    for x in range(10):
        tsum = tsum + random.randint(0, 1)
    if (tsum % 10) > v:
        print("Computer plays first\n")
        computer = STATEX
        human = STATEO
    else:
        print("You play first\n")
        computer = STATEO
        human = STATEX
    return (computer, human)


# human move
def human_move(grid, move):
    print("Your Chance")
    while True:
        place = int(input())
        if grid[int(place / 3)][place % 3] == 2:
            grid[int(place / 3)][place % 3] = move
            break
        else:
            print("illegal move, choose another position")
    return grid

# computer move
def computer_move(grid, c_moves, move):
    itr = 0
    while True:
        if grid[c_moves[itr][0]][c_moves[itr][1]] == 2:
            grid[c_moves[itr][0]][c_moves[itr][1]] = move
            break
        itr = itr + 1
    return grid

# computer random move
def computer_random_move(grid, c_moves, move):
    print("Computer's Chance")
    while True:
        itr = random.randint(0, 8)
        if grid[c_moves[itr][0]][c_moves[itr][1]] == 2:
            grid[c_moves[itr][0]][c_moves[itr][1]] = move
            break
    return grid

# count to value converter
def ctv_converter(score, computer):
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


# generate game tree
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
            visual = board_visualizer(t)
            print_board(visual)
    return t_config


# heuristic evaluator
def heuristic(grid, computer):
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
        # main diagonal
        if grid[i][i] == 5:
            score[0][6] = score[0][6] + 1
        elif grid[i][i] == 3:
            score[1][6] = score[1][6] + 1
        # opposite diagonal
        if grid[i][j] == 5:
            score[0][7] = score[0][7] + 1
        elif grid[i][j] == 3:
            score[1][7] = score[1][7] + 1
        j = j - 1
    if score[0][6] != 0 and score[1][6] != 0:
            score[0][6], score[1][6] = (0,0)
    if score[0][7] != 0 and score[1][7] != 0:
        score[0][7], score[1][7] = (0, 0)
    # count to value converter
    print(score)
    score = ctv_converter(score, computer)
    print(score)
    # sum up the score of a configuration
    for i in range(8):
        final_score = final_score + score[0][i] + score[1][i]
    return final_score


# mini-max wrapper
def minimax_wrapper(grid, move, level, itr, count, computer):
    if level > itr and count < 9:
        # generate all possible board configurations and store them in a list
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

        # create a corresponding score list
        score = []
        for i in range(0, len(f_config)):
            score.append(heuristic(f_config[i], computer))

        # choose best score according to turn, mini-max
        # Computer is X
        max_index = -1
        min_index = -1
        if move == STATEX:
            max_val = -10000
            for i in range(len(f_config)):
                if max_val < score[i]:
                    max_val = score[i]
                    max_index = i

        # Computer is O
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

        # if itr == 1:
        #     if min_index != -1:
        #         grid = t_config[min_index]
        #     else:
        #         grid = t_config[max_index]
        # else:
        #     if min_index != -1:
        #         grid = f_config[min_index]
        #     else:
        #         grid = f_config[max_index]

    return grid


# win condition checker
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

# update values and check win condtion e-m-h-modes
def update(grid, move, count, computer, human):
    # modify
    win_condition = win(grid, move)
    count = count + 1
    if move == STATEX:
        move = STATEO
    else:
        move = STATEX

    # print board
    print_wrapper(grid)

    # check if game over
    over = 0
    if (win_condition == 1 and computer == STATEX) or (win_condition == -1 and computer == STATEO):
        print("Computer Won")
        over = 1
    elif (win_condition == 1 and human == STATEX) or (win_condition == -1 and human == STATEO):
        print("You Won")
        over = -1
    elif count == 9:
        print("Match Drawn")
        over = 2
    return (grid, move, count, over)
