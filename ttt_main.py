from ttt_helper import view_board_positions
from hvh import play_hvh
from  easy_mode import play_easy
from medium_mode import play_ai
from auto_play import auto_play_wrapper



def wrapper():
    # select game mode
    while True:
        print("""Select Game Mode
                 1 - Human vs Human
                 2 - Easy 
                 3 - Medium
                 4 - Hard
                 5 - auto-play 
                 6 - View Board Positions
              """)
        mode = input()

        # launch game
        if mode == '1':
            play_hvh()
        elif mode == '2':
            play_easy()
        elif mode == '3':
            play_ai(2)
        elif mode == '4':
            play_ai(3)
        elif mode == '5':
            (count_wins, count_loses, count_draws) = auto_play_wrapper(epoch=100,n_epoch=100)
            print("count_wins: ",count_wins,"count_loses: ",count_loses,"count_draws: ",count_draws,sep='\n')
        elif mode == '6':
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
        else:
            print("Choose a valid Game Mode! ")

        # end game replay or quit option
        print("Do you want to play again ? y/n")
        ch = input()
        if ch == 'n':
            break

# run the main function
wrapper()
