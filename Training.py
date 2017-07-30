
from Board import Board
from AI import *
import matplotlib.pyplot as plt


def play_n_games(player1, player2, num_games, move_limit):
    """
    [[game1_outcome, num_moves, num_own_pieces, num_opp_pieces, num_own_kings, num_opp_kings]...]
    outcome:
    0 - виграш, 1 - програш, 2 - нічия, 3 - ліміт ходів
    """
    game_board = Board()
    player1.set_board(game_board)
    player2.set_board(game_board)
     
    players_move = player1
    outcome_counter = [[-1,-1,-1,-1,-1,-1] for j in range(num_games)] 
    for j in range(num_games):
        move_counter = 0
        while not game_board.is_game_over() and move_counter < move_limit:
            game_board.make_move(players_move.get_next_move())
             
            move_counter = move_counter + 1
            if players_move is player1:
                players_move = player2
            else:
                players_move = player1
        else:
            piece_counter = get_number_of_pieces_and_kings(game_board.spots)
            if piece_counter[0] != 0 or piece_counter[2] != 0:
                if piece_counter[1] != 0 or piece_counter[3] != 0:
                    if move_counter == move_limit:
                        outcome_counter[j][0] = 3
                    else:
                        outcome_counter[j][0] = 2
                else:
                    outcome_counter[j][0] = 0
#                     if (j+1)%100==0:
#                         print("Player 1 won game #" + str(j + 1) + " in " + str(move_counter) + " turns!")
            else:
                outcome_counter[j][0] = 1
#                 if (j+1)%100==0:
#                     print("Player 2 won game #" + str(j + 1) + " in " + str(move_counter) + " turns!")
            outcome_counter[j][1] = move_counter
            outcome_counter[j][2] = piece_counter[0]
            outcome_counter[j][3] = piece_counter[1]
            outcome_counter[j][4] = piece_counter[2]
            outcome_counter[j][5] = piece_counter[3]
             
            player1.game_completed()
            player2.game_completed()
            game_board.reset_board()
     
    return outcome_counter

def pretty_outcome_display(outcomes):
    """
    Вивід результатів

    """
    game_wins = [0,0,0,0]
    total_moves = 0
    max_moves_made = float("-inf")
    min_moves_made = float("inf")
    for outcome in outcomes:
        total_moves = total_moves + outcome[1]
        if outcome[1] < min_moves_made:
            min_moves_made = outcome[1]
        if outcome[1] > max_moves_made:
            max_moves_made = outcome[1]
        
        game_wins[outcome[0]] = game_wins[outcome[0]] + 1
    
    print("Games Played: ".ljust(35), len(outcomes))
    print("Player 1 wins: ".ljust(35), game_wins[0])
    print("Player 2 wins: ".ljust(35), game_wins[1])
    print("Games exceeded move limit: ".ljust(35), game_wins[3])
    print("Games tied: ".ljust(35), game_wins[2])
    print("Total moves made: ".ljust(35), total_moves)  
    print("Average moves made: ".ljust(35), total_moves/len(outcomes))
    print("Max moves made: ".ljust(35), max_moves_made)
    print("Min moves made: ".ljust(35), min_moves_made)


LEARNING_RATE = .01  
DISCOUNT_FACTOR = .3
NUM_GAMES_TO_TRAIN = 1000
NUM_TRAINING_ROUNDS = 10   
NUM_VALIDATION_GAMES = 200
TRAINING_RANDOM_MOVE_PROBABILITY = .25
ALPHA_BETA_DEPTH = 2
TRAINING_MOVE_LIMIT = 500
VALIDATION_MOVE_LIMIT = 600
PLAYER1 = Q_Learning_AI(True, LEARNING_RATE, DISCOUNT_FACTOR, the_random_move_probability=TRAINING_RANDOM_MOVE_PROBABILITY)#, info_location="data.json")
PLAYER2 = Alpha_beta(False, ALPHA_BETA_DEPTH)
PLAYER3 = Alpha_beta(False, 1)
PLAYER4 = Alpha_beta(False, 3)
training_info = []


training_info = []
validation_info = []
for j in range(NUM_TRAINING_ROUNDS):
    training_info.extend(play_n_games(PLAYER1, PLAYER2, NUM_GAMES_TO_TRAIN, TRAINING_MOVE_LIMIT))
    PLAYER1.print_transition_information(PLAYER1.get_transitions_information())
    PLAYER1.set_random_move_probability(0)
    PLAYER1.set_learning_rate(0)
    print("Тестування: ")
    validation_info.extend(play_n_games(PLAYER1, PLAYER3, NUM_VALIDATION_GAMES, VALIDATION_MOVE_LIMIT))
    print("Раунд " + str(j+1) + " завершено!")
    PLAYER1.set_random_move_probability(TRAINING_RANDOM_MOVE_PROBABILITY)
    PLAYER1.set_learning_rate(LEARNING_RATE)
    #print("")
    #PLAYER1.print_transition_information(PLAYER1.get_transitions_information())
    print("")
    PLAYER1.save_transition_information()


pretty_outcome_display(training_info)
print("")
pretty_outcome_display(validation_info)

'''
validation_info = []

PLAYER1.print_transition_information(PLAYER1.get_transitions_information())
PLAYER1.set_random_move_probability(0)
PLAYER1.set_learning_rate(0)
validation_info.extend(play_n_games(PLAYER1, PLAYER3, NUM_VALIDATION_GAMES, VALIDATION_MOVE_LIMIT))
PLAYER1.set_random_move_probability(TRAINING_RANDOM_MOVE_PROBABILITY)
PLAYER1.set_learning_rate(LEARNING_RATE)
#print("")
#PLAYER1.print_transition_information(PLAYER1.get_transitions_information())
print("")
PLAYER1.save_transition_information()

print("")
pretty_outcome_display(validation_info)

'''

