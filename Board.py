

import math
import copy
from functools import reduce
from tkinter import *
import random
import time

class Board:

    EMPTY_SPOT = 0
    P1 = 1
    P2 = 2
    P1_K = 3
    P2_K = 4
    BACKWARDS_PLAYER = P2
    HEIGHT = 8
    WIDTH = 4
    
    
    def __init__(self, old_spots=None, the_player_turn=True):

        self.player_turn = the_player_turn 
        if old_spots is None:   
            self.spots = [[j, j, j, j] for j in [self.P1, self.P1, self.P1, self.EMPTY_SPOT, self.EMPTY_SPOT, self.P2, self.P2, self.P2]]
            print(self.spots)
        else:
            self.spots = old_spots


    def reset_board(self):

        self.spots = Board().spots
        
    
    def is_game_over(self):

        if not self.get_possible_next_moves():
            return True
        return False


    def not_spot(self, loc):

        if len(loc) == 0 or loc[0] < 0 or loc[0] > self.HEIGHT - 1 or loc[1] < 0 or loc[1] > self.WIDTH - 1:
            return True
        return False
    
    
    def get_spot_info(self, loc):
    
        return self.spots[loc[0]][loc[1]]
    
    
    def forward_n_locations(self, start_loc, n, backwards=False):
       #Можливі ходи по діагоналі
        if n % 2 == 0:
            temp1 = 0
            temp2 = 0
        elif start_loc[0] % 2 == 0:
            temp1 = 0
            temp2 = 1 
        else:
            temp1 = 1
            temp2 = 0

        answer = [[start_loc[0], start_loc[1] + math.floor(n / 2) + temp1], [start_loc[0], start_loc[1] - math.floor(n / 2) - temp2]]

        if backwards: 
            answer[0][0] = answer[0][0] - n
            answer[1][0] = answer[1][0] - n
        else:
            answer[0][0] = answer[0][0] + n
            answer[1][0] = answer[1][0] + n

        if self.not_spot(answer[0]):
            answer[0] = []
        if self.not_spot(answer[1]):
            answer[1] = []
            
        return answer
    

    def get_simple_moves(self, start_loc):
        #Можливі ходи в місця, які не зайняті чужими шашками

        if self.spots[start_loc[0]][start_loc[1]] > 2:
            next_locations = self.forward_n_locations(start_loc, 1)
            next_locations.extend(self.forward_n_locations(start_loc, 1, True))
        elif self.spots[start_loc[0]][start_loc[1]] == self.BACKWARDS_PLAYER:
            next_locations = self.forward_n_locations(start_loc, 1, True)  
        else:
            next_locations = self.forward_n_locations(start_loc, 1)
        

        possible_next_locations = []

        for location in next_locations:
            if len(location) != 0:
                if self.spots[location[0]][location[1]] == self.EMPTY_SPOT:
                    possible_next_locations.append(location)
            
        return [[start_loc, end_spot] for end_spot in possible_next_locations]      
           
     
    def get_capture_moves(self, start_loc, move_beginnings=None):

        if move_beginnings is None:
            move_beginnings = [start_loc]
            
        answer = []
        if self.spots[start_loc[0]][start_loc[1]] > 2:  
            next1 = self.forward_n_locations(start_loc, 1)
            next2 = self.forward_n_locations(start_loc, 2)
            next1.extend(self.forward_n_locations(start_loc, 1, True))
            next2.extend(self.forward_n_locations(start_loc, 2, True))
        elif self.spots[start_loc[0]][start_loc[1]] == self.BACKWARDS_PLAYER:
            next1 = self.forward_n_locations(start_loc, 1, True)
            next2 = self.forward_n_locations(start_loc, 2, True)
        else:
            next1 = self.forward_n_locations(start_loc, 1)
            next2 = self.forward_n_locations(start_loc, 2)
  
        for j in range(len(next1)):
            if (not self.not_spot(next2[j])) and (not self.not_spot(next1[j])) : 
                if self.get_spot_info(next1[j]) != self.EMPTY_SPOT and self.get_spot_info(next1[j]) % 2 != self.get_spot_info(start_loc) % 2:  
                    if self.get_spot_info(next2[j]) == self.EMPTY_SPOT:  
                        temp_move1 = copy.deepcopy(move_beginnings)
                        temp_move1.append(next2[j])
                        
                        answer_length = len(answer)
                        
                        if self.get_spot_info(start_loc) != self.P1 or next2[j][0] != self.HEIGHT - 1: 
                            if self.get_spot_info(start_loc) != self.P2 or next2[j][0] != 0: 

                                temp_move2 = [start_loc, next2[j]]
                                
                                temp_board = Board(copy.deepcopy(self.spots), self.player_turn)
                                temp_board.make_move(temp_move2, False)

                                answer.extend(temp_board.get_capture_moves(temp_move2[1], temp_move1))
                                
                        if len(answer) == answer_length:
                            answer.append(temp_move1)
                            
        return answer
    
        
    def get_possible_next_moves(self):
        piece_locations = []
        for j in range(self.HEIGHT):
            for i in range(self.WIDTH):
                if (self.player_turn == True and (self.spots[j][i] == self.P1 or self.spots[j][i] == self.P1_K)) or (self.player_turn == False and (self.spots[j][i] == self.P2 or self.spots[j][i] == self.P2_K)):
                    piece_locations.append([j, i])
                    
        try:  
            capture_moves = list(reduce(lambda a, b: a + b, list(map(self.get_capture_moves, piece_locations)))) 

            if len(capture_moves) != 0:
                return capture_moves

            return list(reduce(lambda a, b: a + b, list(map(self.get_simple_moves, piece_locations)))) 
        except TypeError:
            return []
    
    
    def make_move(self, move, switch_player_turn=True):

        if abs(move[0][0] - move[1][0]) == 2:
            for j in range(len(move) - 1):
                if move[j][0] % 2 == 1:
                    if move[j + 1][1] < move[j][1]:
                        middle_y = move[j][1]
                    else:
                        middle_y = move[j + 1][1]
                else:
                    if move[j + 1][1] < move[j][1]:
                        middle_y = move[j + 1][1]
                    else:
                        middle_y = move[j][1]
                        
                self.spots[int((move[j][0] + move[j + 1][0]) / 2)][middle_y] = self.EMPTY_SPOT
                
                
        self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.spots[move[0][0]][move[0][1]]
        if move[len(move) - 1][0] == self.HEIGHT - 1 and self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] == self.P1:
            self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.P1_K
        elif move[len(move) - 1][0] == 0 and self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] == self.P2:
            self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.P2_K
        else:
            self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.spots[move[0][0]][move[0][1]]
        self.spots[move[0][0]][move[0][1]] = self.EMPTY_SPOT
                
        if switch_player_turn:
            self.player_turn = not self.player_turn
       

    def get_potential_spots_from_moves(self, moves):

        if moves is None:
            return self.spots
        answer = []
        for move in moves:
            original_spots = copy.deepcopy(self.spots)
            self.make_move(move, switch_player_turn=False)
            answer.append(self.spots) 
            self.spots = original_spots 
        return answer
        
        
    def insert_pieces(self, pieces_info):
        
        for piece_info in pieces_info:
            self.spots[piece_info[0]][piece_info[1]] = piece_info[2]
        
    
    def get_symbol(self, location):

        if self.spots[location[0]][location[1]] == self.EMPTY_SPOT:
            return " "
        elif self.spots[location[0]][location[1]] == self.P1:
            return "o"
        elif self.spots[location[0]][location[1]] == self.P2:
            return "x"
        elif self.spots[location[0]][location[1]] == self.P1_K:
            return "O"
        else:
            return "X"

    def get_spot(self, location):

        if self.spots[location[0]][location[1]] == self.EMPTY_SPOT:
            return 0
        elif self.spots[location[0]][location[1]] == self.P1:
            return 1
        elif self.spots[location[0]][location[1]] == self.P2:
            return 3
        elif self.spots[location[0]][location[1]] == self.P1_K:
            return 2
        else:
            return 4

    def getBoard(self):
        mass = []
        for j in range(self.HEIGHT):
            temp = []
            if j % 2 == 1:
                temp.append(0)
            for i in range(self.WIDTH):
                temp.append(self.get_spot([j,i]))
                if i != 3 or j % 2 != 1:
                    temp.append(0)
            mass.append(temp)
        print(mass)
        return mass



    def print_board(self):
 
        mass = []
        f = open('text.txt', 'a')
        norm_line = "|---|---|---|---|---|---|---|---|"
        print(norm_line)
        f.write(norm_line + '\n')
        for j in range(self.HEIGHT):
            if j % 2 == 1:
                temp_line = "|///|"
                temp_numb = 0
            else:
                temp_line = "|"
            for i in range(self.WIDTH):
                temp_line = temp_line + " " + self.get_symbol([j, i]) + " |"
                temp_numb = self.get_spot([j,i])
                if i != 3 or j % 2 != 1:  
                    temp_line = temp_line + "///|"
                    temp_numb = 0
            print(temp_line)
            mass.append(temp_numb)
            f.write(temp_line + '\n')
            print(norm_line)  
            f.write(norm_line + '\n')
        f.write('\n')
        print('\n')
        f.close()    
        






    
    




