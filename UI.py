from tkinter import *
import random
import time
import copy
from Board import *
from AI import *

window=Tk()
window.title('Шашки')
table=Canvas(window, width=800,height=800,bg='#FFFFFF')
game_board = Board()
table.pack()

flag = TRUE

LEARNING_RATE = 0 
DISCOUNT_FACTOR = .3
TRAINING_RANDOM_MOVE_PROBABILITY = 0
ALPHA_BETA_DEPTH = 1
Qplayer = Q_Learning_AI(True, LEARNING_RATE, DISCOUNT_FACTOR, the_random_move_probability=TRAINING_RANDOM_MOVE_PROBABILITY, info_location="data.json")
Aplayer = Alpha_beta(False, ALPHA_BETA_DEPTH)
Hplayer = Human(False)

Qplayer.set_board(game_board)
Aplayer.set_board(game_board)
Hplayer.set_board(game_board)



def load_images():
    global pawns
    i1=PhotoImage(file="res\\2b.gif")
    i2=PhotoImage(file="res\\2bk.gif")
    i3=PhotoImage(file="res\\2h.gif")
    i4=PhotoImage(file="res\\2hk.gif")
    pawns=[0,i1,i2,i3,i4]


def revers(board):

    board = game_board.getBoard()
    newBoard = [[0] * 8 for i in range(8)]

    for i in range(8):
        for j in range(8):
            newBoard[7-i][j] = board[i][j]
    return newBoard




def capture(x_poz_1,y_poz_1,x_poz_2,y_poz_2):
    global pawns
    global red_frame,g_frame
    newBoard = revers(game_board.getBoard())
    k=100
    x=0
    table.delete('all')
    red_frame=table.create_rectangle(-5, -5, -5, -5,outline="red",width=5)
    g_frame=table.create_rectangle(-5, -5, -5, -5,outline="green",width=5)

    while x<8*k:
        y=1*k
        while y<8*k:
            table.create_rectangle(x, y, x+k, y+k,fill="black")
            y+=2*k
        x+=2*k
    x=1*k
    while x<8*k:
        y=0
        while y<8*k:
            table.create_rectangle(x, y, x+k, y+k,fill="black")
            y+=2*k
        x+=2*k
    
    for y in range(8):
        for x in range(8):
            z=newBoard[y][x]
            if z:  
                if (x_poz_1,y_poz_1)!=(x,y):
                    table.create_image(x*k,y*k, anchor=NW, image=pawns[z])
            
    z=newBoard[y_poz_1][x_poz_1]
    if z:
        table.create_image(x_poz_1*k,y_poz_1*k, anchor=NW, image=pawns[z],tag='ani')
    table.update()
    time.sleep(0.6)


def pozici_1(event):
    x,y=(event.x)//100,(event.y)//100
    table.coords(g_frame,x*100,y*100,x*100+100,y*100+100)

# def pozici_2(event):
#     global flag
#     pole = game_board.getBoard()
#     global poz1_x,poz1_y,poz2_x,poz2_y
#     x,y=(event.x)//100,(event.y)//100
#     if pole[y][x]==1 or pole[y][x]==2:
#         table.coords(kr_ramka,x*100,y*100,x*100+100,y*100+100)
#         poz1_x,poz1_y=x,y
#     else:
#         if poz1_x!=-1:
#             poz2_x,poz2_y=x,y
#             if flag:
#                 hod_player2()
#                 time.sleep(0.5)
#                 if not flag:
#                     hod_player1()
#             poz1_x=-1
#             table.coords(kr_ramka,-5,-5,-5,-5)   


def hod_player1():
    print("HOD PLAYER1:")
    move = Qplayer.get_next_move()
    x_poz_1 = move[0][0]
    y_poz_1 = move[0][1]
    x_poz_2 = move[-1][0]
    y_poz_2 = move[-1][1]
    game_board.make_move(move)
    print(move)
    campture(x_poz_1, y_poz_1, x_poz_2, y_poz_2)

def hod_player2():
    print("HOD PLAYER2: ")
    move = Aplayer.get_next_move()
    x_poz_1 = move[0][0]
    y_poz_1 = move[0][1]
    x_poz_2 = move[-1][0]
    y_poz_2 = move[-1][1]
    print(move)
    game_board.make_move(move)
    capture(x_poz_1, y_poz_1, x_poz_2, y_poz_2)



# def hod_player2():
#     global poz1_x, poz1_y, poz2_x, poz2_y
#     move = [[0] * 2 for i in range(2)]
#     move[0][0] = poz1_x
#     move[0][1] = poz1_y
#     move[-1][0] = poz2_x
#     move[-1][1] = poz2_y
#     print(Hplayer.get_next_move(move))
#     if(Hplayer.get_next_move(move)):
#         game_board.make_move(move)
#         table.update()#!!!обновление



def play_game(event):
    global flag
    #player.set_board(game_board)
    #computer.set_board(game_board)
    players_move = hod_player1()
    game_board.print_board()
    print(game_board.getBoard())
    while not game_board.is_game_over():
        if flag:
            players_move = hod_player2()
            game_board.print_board()
            flag = FALSE
            print(game_board.getBoard())
        else:
            players_move = hod_player1()
            game_board.print_board()
            flag = TRUE

    Qplayer.game_completed()
    Aplayer.game_completed()



load_images()
capture(-1,-1,-1,-1)
print(game_board.print_board())
table.bind("<Motion>", pozici_1)
table.bind("<Button-1>", play_game)

mainloop()






