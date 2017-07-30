
import random
import json
import copy
from ast import literal_eval
from Board import Board
import matplotlib.pyplot as plt
from tkinter import *
import random
import time


class Player:

    def set_board(self, the_board):

        self.board = the_board
    
    def game_completed(self):

        pass
    
    def get_next_move(self):

        pass


def reward_function(state_info1, state_info2):

    if state_info2[1] == 0 and state_info2[3] == 0:
        return 12
    if state_info2[0] == 0 and state_info2[2] == 0:
        return -12
    return state_info2[0]-state_info1[0] + 2*(state_info2[2]-state_info1[2])-(state_info2[1]-state_info1[1])-2*(state_info2[3]-state_info1[3])


class Q_Learning_AI(Player):

    def __init__(self, the_player_id, the_learning_rate, the_discount_factor, info_location=None, the_random_move_probability=0, the_board=None):

        self.random_move_probability = the_random_move_probability  #May want to rename this
        self.learning_rate = the_learning_rate    
        self.discount_factor = the_discount_factor
        self.player_id = the_player_id
        self.board = the_board
        self.pre_last_move_state = None
        self.post_last_move_state = None 
        if not info_location is None:
            self.load_transition_information(info_location)
        else:
            self.transitions = {}

    def set_random_move_probability(self, probability):

        self.random_move_probability = probability


    def set_learning_rate(self, the_learning_rate):

        self.learning_rate = the_learning_rate
    

    def get_states_from_boards_spots(self, boards_spots):
    

        piece_counters = [[0,0,0,0,0,0,0] for j in range(len(boards_spots))] 
        #piece_counters = [[0,0,0,0,0,0,0,0,0] for j in range(len(boards_spots))] 
        for k in range(len(boards_spots)):
            for j in range(len(boards_spots[k])):
                for i in range(len(boards_spots[k][j])):
                    if boards_spots[k][j][i] != 0:
                    
                        piece_counters[k][boards_spots[k][j][i]-1] = piece_counters[k][boards_spots[k][j][i]-1] + 1
                        if (self.player_id and (boards_spots[k][j][i] == 1 or boards_spots[k][j][i] == 3)) or (not self.player_id and (boards_spots[k][j][i] == 2 or boards_spots[k][j][i] == 4)):
                            if i==0 and j%2==0:
                                piece_counters[k][4] = piece_counters[k][4] + 1
                            elif i==3 and j%2==1:
                                piece_counters[k][4] = piece_counters[k][4] + 1
                                
                            piece_counters[k][5] = piece_counters[k][5] + j#%%%%%%%%%%%%%%%%%%%%%%%%%%%%% FOR (2)
                            #piece_counters[k][6] = piece_counters[k][6] + i
                        else: 
                            #piece_counters[k][7] = piece_counters[k][7] + j#%%%%%%%%%%%%%%%%%%%%%%%%%%%%% FOR (2)
                            #piece_counters[k][8] = piece_counters[k][8] + i
                            piece_counters[k][6] = piece_counters[k][6] + j
            
            """
            if piece_counters[k][0] + piece_counters[k][2] != 0: #%%%%%%%%%%%%%%%%%%%%%%%%%%%%% FOR (2)
                piece_counters[k][5] = int(piece_counters[k][5] / (piece_counters[k][0] + piece_counters[k][2]))
                piece_counters[k][6] = int(piece_counters[k][6] / (piece_counters[k][0] + piece_counters[k][2]))
            else:
                piece_counters[k][5] = 0
                piece_counters[k][6] = 0
            if piece_counters[k][1] + piece_counters[k][3] != 0:
                piece_counters[k][7] = int(piece_counters[k][7] / (piece_counters[k][1] + piece_counters[k][3]))
                piece_counters[k][8] = int(piece_counters[k][8] / (piece_counters[k][1] + piece_counters[k][3]))
            else:
                piece_counters[k][7] = 0
                piece_counters[k][8] = 0
            """
            
            if piece_counters[k][0] + piece_counters[k][2] != 0: #%%%%%%%%%%%%%%%%%%%%%%%%%%%%% FOR (2)
                piece_counters[k][5] = int(piece_counters[k][5] / (piece_counters[k][0] + piece_counters[k][2]))
                #piece_counters[k][6] = int(piece_counters[k][6] / (piece_counters[k][0] + piece_counters[k][2]))
            else:
                piece_counters[k][5] = 0
                #piece_counters[k][6] = 0
            if piece_counters[k][1] + piece_counters[k][3] != 0:
                piece_counters[k][6] = int(piece_counters[k][6] / (piece_counters[k][1] + piece_counters[k][3]))
                #piece_counters[k][8] = int(piece_counters[k][8] / (piece_counters[k][1] + piece_counters[k][3]))
            else:
                piece_counters[k][6] = 0
                #piece_counters[k][8] = 0
    
        return [tuple(counter) for counter in piece_counters]
                                 

    def get_desired_transition_between_states(self, possible_state_array, initial_transition_value=5):#%%%%%%%%%%%%%%%%%%%%%%%%%%%%% FOR (1)
        cur_state = tuple(self.get_states_from_boards_spots([self.board.spots])[0])
        done_transitions = {}
        for state in possible_state_array:#%%%%%%%%%%%%%%%%%%%%%%%%%%%%% FOR (1)
            if done_transitions.get((cur_state, tuple(state))) is None:
                if self.transitions.get((cur_state, tuple(state))) is None:
                    self.transitions.update({(cur_state, tuple(state)):initial_transition_value})
                done_transitions.update({(cur_state, tuple(state)):self.transitions.get((cur_state, tuple(state)))})
                
            
        if random != 0 and random.random() < self.random_move_probability:
            try:
                return list(done_transitions.keys())[random.randint(0, len(done_transitions)-1)]
            except:   
                return []
    
        try:
            reverse_dict = {j:i for i,j in done_transitions.items()}
            return reverse_dict.get(max(reverse_dict))
        except:
            return []    
   
   
    def game_completed(self):

        cur_state = self.get_states_from_boards_spots([self.board.spots])[0]
        transition = (self.pre_last_move_state ,self.post_last_move_state)

        self.transitions[transition] = self.transitions[transition] + self.learning_rate * reward_function(transition[0],cur_state)

        self.pre_last_move_state = None
        self.post_last_move_state = None



    def get_transitions_information(self):

        start_of_transitions = {}
        max_value = float("-inf")
        min_value = float("inf")
        total_value = 0
        for k,v in self.transitions.items():
            if start_of_transitions.get(k[0]) is None:
                start_of_transitions.update({k[0]:0})
            #if k[0] not in start_of_transitions:
                #start_of_transitions.append(k[0])
            if v > max_value:
                max_value = v
            if v < min_value:
                min_value = v
            total_value = total_value + v
            
        return [len(self.transitions), len(start_of_transitions), float(total_value/len(self.transitions)), max_value, min_value]
    
    
    def print_transition_information(self, info):

        print("Transition: ".ljust(35), info[0])        
        print("Visited states: ".ljust(35), info[1])
        print("Average transition: ".ljust(35), info[2])
       
    def save_transition_information(self, file_name="data.json"):

        with open(file_name, 'w') as fp:
            json.dump({str(k): v for k,v in self.transitions.items()}, fp)
        
        
    def load_transition_information(self, file_name):

        with open(file_name, 'r') as fp:
            self.transitions = {literal_eval(k): v for k,v in json.load(fp).items()}
        
        
    def get_optimal_potential_value(self, depth):

        answer = float("-inf")
        cur_state = self.get_states_from_boards_spots([self.board.spots])[0]
        for k,v in self.transitions.items():
            if k > answer and v[0] == cur_state:
                answer = k
        
        if answer == float("-inf"):
            return None
        return answer



    def get_next_move(self):#, new_board):

        if self.pre_last_move_state is not None:#%%%%%%%%%%%%%%%%%%%%%%%%%%%% FOR (1)
            cur_state = self.get_states_from_boards_spots([self.board.spots])[0]
    
            transition = (self.pre_last_move_state ,self.post_last_move_state)
            try:# self.transitions.get(transition) is not None:#%%%%%%%%%%%%%%%%%%%%%%%%%%%% FOR (1)
                max_future_state = self.get_optimal_potential_value(1)
                self.transitions[transition] = self.transitions[transition] + self.learning_rate * (reward_function(transition[0],cur_state)+ self.discount_factor* max_future_state - self.transitions[transition])
            except:#%%%%%%%%%%%%%%%%%%%%%%%%%%%% FOR (1)
                self.transitions[transition] = self.transitions[transition] + self.learning_rate * (reward_function(transition[0],cur_state))
        
        
        self.pre_last_move_state = self.get_states_from_boards_spots([self.board.spots])[0]#%%%%%%%%%%%%%%%%%%%%%%%%%%%% FOR (1)
        
        possible_next_moves = self.board.get_possible_next_moves()
        possible_next_states = self.get_states_from_boards_spots(self.board.get_potential_spots_from_moves(possible_next_moves))
        
        self.post_last_move_state = self.get_desired_transition_between_states(possible_next_states)[1]   
        
        considered_moves = []
        for j in range(len(possible_next_states)):
            if tuple(possible_next_states[j]) == self.post_last_move_state:
                considered_moves.append(possible_next_moves[j])
                
                

        #I believe with the updated board.is_game_over() I don't need to use this try statement 
        try:
            return considered_moves[random.randint(0,len(considered_moves)-1)]
        except ValueError:
            return []
            

def get_number_of_pieces_and_kings(spots, player_id=None):

    piece_counter = [0,0,0,0]  
    for row in spots:
        for element in row:
            if element != 0:
                piece_counter[element-1] = piece_counter[element-1] + 1
    
    if player_id == True:
        return [piece_counter[0], piece_counter[2]]
    elif player_id == False:
        return [piece_counter[1], piece_counter[3]]
    else:
        return piece_counter
    

class Alpha_beta(Player):

    def __init__(self, the_player_id, the_depth, the_board=None):

        self.board = the_board
        self.depth = the_depth
        self.player_id = the_player_id

    def alpha_beta(self, board, depth, alpha, beta, maximizing_player):

        if board.is_game_over():
            if get_number_of_pieces_and_kings(board.spots, board.player_turn) == [0,0]:
                if maximizing_player:
                    return -10000000, None  
                else:
                    return 10000000, None
            elif get_number_of_pieces_and_kings(board.spots, not board.player_turn) == [0,0]:
                if maximizing_player:
                    return 1000000, None
                else:
                    return -1000000, None
            else:
                return 0, None

        if depth == 0:
            players_info = get_number_of_pieces_and_kings(board.spots)
            if board.player_turn != maximizing_player:
                return  players_info[1] + 2 * players_info[3] - (players_info[0] + 2 * players_info[2]), None
            return  players_info[0] + 2 * players_info[2] - (players_info[1] + 2 * players_info[3]), None
        possible_moves = board.get_possible_next_moves()

        potential_spots = board.get_potential_spots_from_moves(possible_moves)
        desired_move_index = None
        if maximizing_player:
            v = float('-inf')
            for j in range(len(potential_spots)):
                cur_board = Board(potential_spots[j], not board.player_turn)
                alpha_beta_results = self.alpha_beta(cur_board, depth - 1, alpha, beta, False)
                if v < alpha_beta_results[0]: 
                    v = alpha_beta_results[0]
                    alpha = max(alpha, v)
                    desired_move_index = j
                if beta <= alpha: 
                    break
            if desired_move_index is None:
                return v, None
            return v, possible_moves[desired_move_index]
        else:
            v = float('inf')
            for j in range(len(potential_spots)):
                cur_board = Board(potential_spots[j], not board.player_turn)
                alpha_beta_results = self.alpha_beta(cur_board, depth - 1, alpha, beta, True)
                if v > alpha_beta_results[0]:  
                    v = alpha_beta_results[0]
                    desired_move_index = j
                    beta = min(beta, v)
                if beta <= alpha:
                    break
            if desired_move_index is None:
                return v, None
            return v, possible_moves[desired_move_index]
    
    def get_next_move(self):
        return self.alpha_beta(self.board, self.depth, float('-inf'), float('inf'), self.player_id)[1]

class Human(Player):
    def __init__(self, the_player_id,the_board=None):
        self.board = the_board
        self.player_id = the_player_id

    def get_next_move(self,move):
        print(move)
        print(self.board.get_possible_next_moves())
        possible_moves = self.board.get_possible_next_moves()
        if move in possible_moves:
            return TRUE
        else: 
            return FALSE

        






