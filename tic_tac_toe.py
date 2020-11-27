import random
import copy

# simple h vs h version
# heuristic via table lookup
# heuristic board eval
# rule-based strategy
# mini-max algorithm
# mini-max algorithm + alpha-beta

# player move state
from typing import List, Any

STATEO = 3
STATEX = 5


############### Helper Functions ######################

# initializes tic tac toe grid/board
def setup_tic_tac_toe():
    grid = [[2, 2, 2],
            [2, 2, 2],
            [2, 2, 2]]
    return grid


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


# view tic tac toe board before starting the game
def view_board_positions():
    grid = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    print_board(grid)


# toss function to decide x
def toss():
    print("""
        coin toss to start the game first
        h - heads
        t - tails
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
        return 1
    return -1


# count to value converter
def ctv_converter(score):
    for i in range(8):
        if score[0][i] == 3:
            score[0][i] = 100
        elif score[0][i] == 2:
            score[0][i] = 10
        elif score[0][i] == 1:
            score[0][i] = 1
        elif score[0][i] == 0:
            score[0][i] = 0

    for i in range(8):
        if score[1][i] == 3:
            score[1][i] = -100
        elif score[1][i] == 2:
            score[1][i] = -10
        elif score[1][i] == 1:
            score[1][i] = -1
        elif score[1][i] == 0:
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
            # visual = board_visualizer(t)
            # print_board(visual)
    return t_config


# heuristic evaluator
def heuristic(grid, move):
    final_score = 0
    score = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    for x in range(3):
        for y in range(3):
            if grid[x][y] == 5:
                score[0][x] = score[0][x] + 1
            elif grid[x][y] == 3:
                score[1][x] = score[1][x] + 1

    for y in range(3):
        for x in range(3):
            if grid[x][y] == 5:
                score[0][y + 3] = score[0][y + 3] + 1
            elif grid[x][y] == 3:
                score[1][y + 3] = score[1][y + 3] + 1

    # main diagonal
    if grid[0][0] == 5:
        score[0][6] = score[0][6] + 1

    elif grid[0][0] == 3:
        score[1][6] = score[1][6] + 1

    if grid[1][1] == 5:
        score[0][6] = score[0][6] + 1
        score[0][7] = score[0][7] + 1

    elif grid[1][1] == 3:
        score[1][6] = score[1][6] + 1
        score[1][7] = score[1][7] + 1

    if grid[2][2] == 5:
        score[0][6] = score[0][6] + 1

    elif grid[2][2] == 3:
        score[1][6] = score[1][6] + 1

    ###############################

    #### opposite diagonal ########
    if grid[0][2] == 5:
        score[0][7] = score[0][7] + 1

    elif grid[0][2] == 3:
        score[1][7] = score[1][7] + 1

    if grid[2][0] == 5:
        score[0][7] = score[0][7] + 1

    elif grid[2][0] == 3:
        score[1][7] = score[1][7] + 1

    # count to value converter
    # print(score)
    score = ctv_converter(score)
    # print(score)
    # sum up the score of a configuration
    for i in range(8):
        final_score = final_score + score[0][i] + score[1][i]
    return final_score


# mini-max wrapper
def minimax_wrapper(grid, move, level, itr, count):
    # generate all possible board configurations and store them in a list
    t_config = generateCon(grid, move)
    f_config = t_config
    # print("move {}".format(move))
    # recursive call
    # print("level {}".format(level))
    # print("itr {}".format(itr))
    # print("count {}".format(count))
    if level > itr and count < 9:
        f_config = []
        if move == STATEX:
            move = STATEO
        else:
            move = STATEX
        for i in range(len(t_config)):
            f_config.append(minimax_wrapper(t_config[i], move, level, itr+1, count+1))
        if move == STATEX:
            move = STATEO
        else:
            move = STATEX


    # create a corresponding score list
    score = []
    for i in range(0, len(f_config)):
        score.append(heuristic(f_config[i], move))
        # print("score is {}".format(score[i]))

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
        # print("max val {}".format(max_val))

    # Computer is O
    else:
        min_val = 10000
        for i in range(len(f_config)):
            if min_val > score[i]:
                min_val = score[i]
                min_index = i
        # print("min index {}".format(min_index))
        # print("min val {}".format(min_val))
    if itr == 1:
        if min_index != -1:
            grid = t_config[min_index]
        else:
            grid = t_config[max_index]
    else:
        if min_index != -1:
            grid = f_config[min_index]
        else:
            grid = f_config[max_index]

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


#######################################################

############### H vs H Functions ######################

# testing game mode human vs human version
def play_hvh():
    # set up tic tac toe board
    grid = setup_tic_tac_toe()
    move = STATEX
    count = 0
    visual = board_visualizer(grid)
    print_board(visual)

    while True:
        if move == STATEX:
            print("Player 1 move ")
        else:
            print("Player 2 move ")

        while True:
            place = int(input())
            if place == 10:
                win_condition = 2
            elif place <=8 and grid[int(place / 3)][place % 3] == 2:
                grid[int(place / 3)][place % 3] = move
                break
            else:
                print("illegal move, choose another position")

        # modify
        win_condition = win(grid, move)
        count = count + 1
        if move == STATEX:
            move = STATEO
        else:
            move = STATEX

        # print board
        visual = board_visualizer(grid)
        print_board(visual)

        if win_condition == 1:
            print("Player 1 won")
            break
        elif win_condition == -1:
            print("Player 2 won")
            break
        elif win_condition == 2 or count == 9:
            print("Match Drawn")
            break


#######################################################################

################ Easy-Random move computer player #####################

# not ai, random moves
def play_easy():
    # toss to choose player 1
    if toss() == 1:
        print("Computer plays first\n")
        computer = STATEX
        human = STATEO
    else:
        print("You play first\n")
        computer = STATEO
        human = STATEX
    c_moves = [[1, 1], [0, 0], [0, 2], [2, 0], [2, 2],
               [1, 1], [1, 0], [1, 2], [2, 1]]

    # set up tic tac toe board
    grid = setup_tic_tac_toe()
    count = 0
    move = STATEX
    visual = board_visualizer(grid)
    print_board(visual)

    while True:
        # Computer moves
        if computer == move:
            print("Computer's Chance")
            while True:
                itr = random.randint(0, 8)
                if grid[c_moves[itr][0]][c_moves[itr][1]] == 2:
                    grid[c_moves[itr][0]][c_moves[itr][1]] = move
                    break


        # Human moves
        else:
            print("Your Chance")
            while True:
                place = int(input())
                if grid[int(place / 3)][place % 3] == 2:
                    grid[int(place / 3)][place % 3] = move
                    break
                else:
                    print("illegal move, choose another position")

        # modify
        win_condition = win(grid, move)
        count = count + 1
        if move == STATEX:
            move = STATEO
        else:
            move = STATEX

        # print board
        visual = board_visualizer(grid)
        print_board(visual)

        # check if game over
        if (win_condition == 1 and computer == STATEX) or (win_condition == -1 and computer == STATEO):
            print("Computer Won")
            break
        elif (win_condition == 1 and human == STATEX) or (win_condition == -1 and human == STATEO):
            print("You Won")
            break
        elif count == 9:
            print("Match Drawn")
            break


############################################################################

################ Medium-computer player defends itself #####################

# defend itself, one level lookahead

def play_medium():
    # toss to choose player 1
    if toss() == 1:
        print("Computer plays first\n")
        computer = STATEX
        human = STATEO
    else:
        print("You play first\n")
        computer = STATEO
        human = STATEX

    # set up tic tac toe board
    grid = setup_tic_tac_toe()
    count = 2
    c_moves = [[1, 1], [0, 0], [0, 2], [2, 0], [2, 2],
               [1, 1], [1, 0], [1, 2], [2, 1]]
    move = STATEX
    visual = board_visualizer(grid)
    print_board(visual)

    # first human and computer move
    if computer == STATEX:
        print("Computer's Chance")
        grid[1][1] = STATEX
        visual = board_visualizer(grid)
        print_board(visual)
        print("Your Chance")
        while True:
            place = int(input())
            if grid[int(place / 3)][place % 3] == 2:
                grid[int(place / 3)][place % 3] = STATEO
                break
            else:
                print("illegal move, choose another position")

    else:
        print("Your Chance")
        while True:
            place = int(input())
            if grid[int(place / 3)][place % 3] == 2:
                grid[int(place / 3)][place % 3] = STATEX
                break
            else:
                print("illegal move, choose another position")
        visual = board_visualizer(grid)
        print_board(visual)
        print("Computer's Chance")
        itr = 0
        while True:
            if grid[c_moves[itr][0]][c_moves[itr][1]] == 2:
                grid[c_moves[itr][0]][c_moves[itr][1]] = STATEO
                break
            itr = itr + 1

    visual = board_visualizer(grid)
    print_board(visual)

    # following moves, 1 level look-ahead
    while True:
        # human plays
        if human == move:
            print("Your Chance")
            while True:
                place = int(input())
                if grid[int(place / 3)][place % 3] == 2:
                    grid[int(place / 3)][place % 3] = move
                    break
                else:
                    print("illegal move, choose another position")

        # computer plays
        else:
            print("Computer's Chance")
            if count == 8:
                itr = 0
                while True:
                    if grid[c_moves[itr][0]][c_moves[itr][1]] == 2:
                        grid[c_moves[itr][0]][c_moves[itr][1]] = move
                        break
                    itr = itr + 1
            else:
                grid = minimax_wrapper(grid, computer, 2, 1, count+1)

        # modify
        win_condition = win(grid, move)
        count = count + 1
        if move == STATEX:
            move = STATEO
        else:
            move = STATEX

        # print board
        visual = board_visualizer(grid)
        print_board(visual)

        # check if game over
        if (win_condition == 1 and computer == STATEX) or (win_condition == -1 and computer == STATEO):
            print("Computer Won")
            break
        elif (win_condition == 1 and human == STATEX) or (win_condition == -1 and human == STATEO):
            print("You Won")
            break
        elif count == 9:
            print("Match Drawn")
            break

        # covert mini-max to alpha-beta


############################################################################

################ Hard-computer player tries to win #########################

# try for fork and defends itself - two level lookahead
def play_hard():
    # toss to choose player 1
    if toss() == 1:
        print("Computer plays first\n")
        computer = STATEX
        human = STATEO
    else:
        print("You play first\n")
        computer = STATEO
        human = STATEX

    # set up tic tac toe board
    grid = setup_tic_tac_toe()
    count = 2
    c_moves = [[1, 1], [0, 0], [0, 2], [2, 0], [2, 2],
               [1, 1], [1, 0], [1, 2], [2, 1]]
    move = STATEX
    visual = board_visualizer(grid)
    print_board(visual)

    # first human and computer move
    if computer == STATEX:
        print("Computer's Chance")
        grid[1][1] = STATEX
        visual = board_visualizer(grid)
        print_board(visual)
        print("Your Chance")
        while True:
            place = int(input())
            if grid[int(place / 3)][place % 3] == 2:
                grid[int(place / 3)][place % 3] = STATEO
                break
            else:
                print("illegal move, choose another position")

    else:
        print("Your Chance")
        while True:
            place = int(input())
            if grid[int(place / 3)][place % 3] == 2:
                grid[int(place / 3)][place % 3] = STATEX
                break
            else:
                print("illegal move, choose another position")
        visual = board_visualizer(grid)
        print_board(visual)
        print("Computer's Chance")
        itr = 0
        while True:
            if grid[c_moves[itr][0]][c_moves[itr][1]] == 2:
                grid[c_moves[itr][0]][c_moves[itr][1]] = STATEO
                break
            itr = itr + 1

    visual = board_visualizer(grid)
    print_board(visual)

    # following moves, 1 level look-ahead
    while True:
        # human plays
        if human == move:
            print("Your Chance")
            while True:
                place = int(input())
                if grid[int(place / 3)][place % 3] == 2:
                    grid[int(place / 3)][place % 3] = move
                    break
                else:
                    print("illegal move, choose another position")

        # computer plays
        else:
            print("Computer's Chance")
            if count == 8:
                itr = 0
                while True:
                    if grid[c_moves[itr][0]][c_moves[itr][1]] == 2:
                        grid[c_moves[itr][0]][c_moves[itr][1]] = move
                        break
                    itr = itr + 1
            else:
                grid = minimax_wrapper(grid, computer, 3, 1, count+1)

        # modify
        win_condition = win(grid, move)
        count = count + 1
        if move == STATEX:
            move = STATEO
        else:
            move = STATEX

        # print board
        visual = board_visualizer(grid)
        print_board(visual)

        # check if game over
        if (win_condition == 1 and computer == STATEX) or (win_condition == -1 and computer == STATEO):
            print("Computer Won")
            break
        elif (win_condition == 1 and human == STATEX) or (win_condition == -1 and human == STATEO):
            print("You Won")
            break
        elif count == 9:
            print("Match Drawn")
            break


############################################################################

################ Main function #############################################

def wrapper():
    # select game mode
    while True:
        print("""Select Game Mode
                 1 - Human vs Human
                 2 - Easy Level vs Computer
                 3 - Medium Level vs Computer
                 4 - Hard Level vs Computer
                 5 - View Board Postions
                 6 - Exit
              """)
        mode = input()

        # launch game
        if mode == '1':
            while True:
                play_hvh()
                print("Do you want to play again ? y/n")
                ch = input()
                if ch == 'n':
                    break

        elif mode == '2':
            while True:
                play_easy()
                print("Do you want to play again ? y/n")
                ch = input()
                if ch == 'n':
                    break

        elif mode == '3':
            while True:
                play_medium()
                print("Do you want to play again ? y/n")
                ch = input()
                if ch == 'n':
                    break

        elif mode == '4':
            while True:
                play_hard()
                print("Do you want to play again ? y/n")
                ch = input()
                if ch == 'n':
                    break

        elif mode == '5':
            view_board_positions()
            print("""
                    Press m for main menu
                    Press anything else to quit
                    """)
            ch = input()
            if ch == 'm':
                continue
            else:
                break

        elif mode == '6':
            break

        else:
            print("Please Choose a valid Game Mode! ")



############################################################################

# run the main function
wrapper()
