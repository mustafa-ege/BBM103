# b2210356088 Mustafa Ege

# The code prints the errors in the beginning of the output because i check for the errors in the functions which are in the beginning of the code.
# The code continue to play the game after the error but error message is in the beginnging instead of that round.
# !!!

import sys
import os

output = open('Battleship.out','w')

def printer(text): #function for printing to terminal and to the output file at the same time
    output.write(text)
    print(text,end='')

except_list = []
input_list = ['Player1.txt','Player2.txt','Player1.in','Player2.in']
for input_file in input_list: # if required input files doesn't exist it adds them to the except list
    if not os.path.exists(input_file):
        except_list.append(input_file)

# checks if all of the required files ('Player1.txt','Player2.txt','Player1.in','Player1.in') exists or not
try:
    if except_list != []:
        raise IOError
except:
    printer('IOError: input file(s) {} is/are not reachable.\n'.format(except_list))
    sys.exit()

try:   #checks if terminal input file names exists or not in the file directory
    player1_start = open(sys.argv[1],'r')
    player2_start = open(sys.argv[2],'r')
    player1_input = open(sys.argv[3],'r')
    player2_input = open(sys.argv[4],'r')
except Exception as e:
    printer(f'IOError: input file(s) {e.filename} is/are not reachable.\n' )
    sys.exit()

def player_board(player_number):
    input_list = player_number.read().splitlines() 
    player_map = list() #multi-dimensional list for the first appearance of the player's board
    for line in input_list:
        with_hyphen = ['-' if i =='' else i for i in line.split(';')]
        player_map.append(with_hyphen) #splitting the input with ; semicolons and making another list
    return player_map

player1_board = (player_board(player1_start))
player2_board = (player_board(player2_start))

lettervalue = dict(zip("ABCDEFGHIJ",range(0,10)))   #assigning numbers to letters from A to J
lettervaluereverse = dict(zip(range(0,10), "ABCDEFGHIJ"))   #assigning numbers to letters from A to J

def player_moves(player_number):    #function for making a list containing all the moves by a player
    input_list = player_number.read().rstrip(';').split(';')
    moves_list = list()
    for i in input_list:
        try:    #catches if the input is missing arguments (index error)
            two_digit = i.split(',') 
            if len(two_digit) < 2:
                raise IndexError
            elif two_digit[0] == '' or two_digit[1] == '':
                raise IndexError

            second_value = None
            try: 
                second_value = int(two_digit[1])  
            except:
                pass
            #catches if the input contains values which can not be interpreted by the code
            if len(two_digit[0]) <= 2 and len(two_digit[1]) ==1:
                if isinstance(second_value,int):
                    raise ValueError
                elif len(two_digit) >2:
                    raise ValueError
            else:
                raise ValueError

            two_digit[0] = int(two_digit[0])-1  #converting from str to int   
            assert two_digit[0] in range(0,10)  
            assert two_digit[1] in ['A','B','C','D','E','F','G','H','I','J']
            two_digit[1] = lettervalue[two_digit[1]] #using integers instead of letters like A B .. J
            moves_list.append(two_digit)
        except ValueError :
            printer(f'ValueError: ({i}) is a wrong input. There should be two values and first value should be a number(integer) and second should be a letter(string) like (4,C)\n\n')
            continue
        except IndexError:
            printer(f'IndexError: ({i}) is a wrong input. It is missing one or more arguments. There should be two values like (4,C)\n\n')
            continue
        except AssertionError:
            printer('AssertionError: Invalid Operation.\n\n')
            continue
    return moves_list #moves_list is a nested list to have the player's moves 

player1_moves = player_moves(player1_input)
player2_moves = player_moves(player2_input)

player1_empty_board = [['-' for i in range(10)]for i in range(10)] #empty lists without the locations of ships
player2_empty_board = [['-' for i in range(10)]for i in range(10)]

optional_input1 = open('OptionalPlayer1.txt','r')
optional_input2 = open('OptionalPlayer2.txt','r')

# function to make list for battleships and patrol boats but this function only records the first square and the position of the boat
def optinal_input(input):
    battleship_dic_list = list()
    for line in input.read().splitlines():
        battheship_dic = dict()
        ship_feature = line.split(':')[1].rstrip(';').split(';')
        index1,index2 =int(ship_feature[0].split(',')[0])-1,lettervalue[ship_feature[0].split(',')[1]]
        ship_feature[0]=[]
        ship_feature[0].append(index1)
        ship_feature[0].append(index2)
        battheship_dic[line.split(':')[0]] = ship_feature
        battleship_dic_list.append(battheship_dic)
    return battleship_dic_list

def ship_completer(ships): #adds the remaning coordinates of ships like patrolboat and battleship to the list
    def coordinate_adder(ship_type):
        if ship_type == 'B':
            end = 4
        elif ship_type == 'P':
            end = 2
        if ship[key][1] == 'right':
            for column in range(1,end):
                coordinate = [ship[key][0][0],ship[key][0][1]+column]
                ship[key].append(coordinate)
            ship[key].remove('right')
        elif ship[key][1] == 'down':
            for column in range(1,end):
                coordinate = [ship[key][0][0]+column,ship[key][0][1]]
                ship[key].append(coordinate)
            ship[key].remove('down')

    for ship in ships:
        for key in ship:
            if key[0] == 'B':
                coordinate_adder('B')
            elif key[0] == 'P':
                coordinate_adder('P')
    return ships[0:2],ships[2:6]

player1_battleships,player1_patrolboats = ship_completer(optinal_input(optional_input1))
player2_battleships,player2_patrolboats = ship_completer(optinal_input(optional_input2))
battle_ships = [player1_battleships] + [player2_battleships]
patrol_boats = [player1_patrolboats] + [player2_patrolboats]

player1_ships, player2_ships = dict(),dict()
def ship_list(player_ships): #creating a dictionary to hold how many ships a player has
    for i in ['C','D','S']:
        player_ships[i] = 1
    player_ships['P'] = 4
    player_ships['B'] = 2  
ship_list(player1_ships)  
ship_list(player2_ships) 
players_ships = [player1_ships,player2_ships]

def attack(movelist,playerboard,playeremptyboard,round): #to attack a square on the grid and change the info of that square
    global player1_board,player2_board,player1_empty_board,player2_empty_board
    line = movelist[round][0]
    column = movelist[round][1]
    try:
        if playerboard[line][column] != '-':
            assert playerboard[line][column] != 'X' and playerboard[line][column] != 'O'
            playerboard[line][column] = 'X'
            playeremptyboard[line][column] = 'X'
        else:
            assert playerboard[line][column] != 'X' and playerboard[line][column] != 'O'
            playerboard[line][column] = 'O'
            playeremptyboard[line][column] = 'O'
    except AssertionError:
        printer('AssertionError: Invalid Operation.\n\n')

#to determine if the ship type has sunk or not and it works differently if the ship type has more than one ship (battleship, patrol boat)
def sunken_ship(ship_type,player_number,player_boards=None):
    def remaining_ship_counter(ship_type): # counts the number of the ship type in whole player board
        remaining = 0
        for line in player_boards:
            remaining += (line.count(ship_type))
        return remaining
    if ship_type == 'C' or ship_type== 'D' or ship_type =='S':
        if remaining_ship_counter(ship_type) != 0:
            return '-'
        else:
            players_ships[player_number-1][ship_type] = 0 
            return 'X'
    elif ship_type == 'B': 
        sunk = 0
        for boat in battle_ships[player_number-1]:
            for boatname in boat:
                if boat[boatname].count('X') == 4: # checks if 4 of the squares has sunk or not of the battleship
                    sunk += 1
                    if sunk == 2:  # if 2 boat has sunk it makes the number of the player's ship to zero
                        players_ships[player_number-1][ship_type] = 0  
        return sunk
    elif ship_type == 'P':
        sunk = 0
        for boat in patrol_boats[player_number-1]:
            for boatname in boat:
                if boat[boatname].count('X') == 2: # checks if 2 of the squares has sunk or not of the patrol boat
                    sunk += 1
                    if sunk == 4: # if 4 boat has sunk it makes the number of the player's ship to zero
                        players_ships[player_number-1][ship_type] = 0
        return sunk
 
def special_sunken_ship_caller():  # to change the special ships' information according to player boards
    def special_sunken_ship(special_ship_list,player_board): 
        for ship in special_ship_list:
            for i in ship:
                for coordinate in ship[i]:
                    if coordinate == 'X':
                        continue
                    if player_board[coordinate[0]][coordinate[1]] == 'X':
                        special_ship_list[special_ship_list.index(ship)][i][ship[i].index(coordinate)] ='X'
    special_sunken_ship(player1_battleships,player1_empty_board)
    special_sunken_ship(player1_patrolboats,player1_empty_board)
    special_sunken_ship(player2_battleships,player2_empty_board)
    special_sunken_ship(player2_patrolboats,player2_empty_board)

def all_sunk_ship_caller(): # calling every remaining ship function in one place
    special_sunken_ship_caller()
    sunken_ship('C',1,player1_board),sunken_ship('C',2,player2_board)
    sunken_ship('B',1),sunken_ship('B',2)
    sunken_ship('D',1,player1_board),sunken_ship('D',2,player2_board)
    sunken_ship('S',1,player1_board),sunken_ship('S',2,player2_board)
    sunken_ship('P',1),sunken_ship('P',2)

def print_grid(player1_empty_board,player2_empty_board,player,condition,round=None):
    def boards(): #  prints the grid with letters and numbers in the corners and x and o's later it prints remaining ships
        letters = [' ','A','B','C','D','E','F','G','H','I','J']
        printer('{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<1}\t\t'.format(*letters))
        printer('{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<1}\n'.format(*letters))
        for number in range(10):
            printer('{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<1}\t\t'.format(number+1,*player1_empty_board[number]))
            printer('{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<1}\n'.format(number+1,*player2_empty_board[number]))
        printer('\n')
        battleship_sign1,battleship_sign2 = (sunken_ship('B',1)*'X '+ (2-(sunken_ship('B',1)))*'- '),(sunken_ship('B',2)*'X '+ (2-(sunken_ship('B',2)))*'- ')
        patrol_sign1, patrol_sign2 = (sunken_ship('P',1)*'X '+ (4-(sunken_ship('P',1)))*'- '),(sunken_ship('P',2)*'X '+ (4-(sunken_ship('P',2)))*'- ')
        printer('Carrier\t\t{}\t\t\t\tCarrier\t\t{}\n'.format(sunken_ship('C',1,player1_board),sunken_ship('C',2,player2_board)))
        printer('Battleship\t{}\t\t\t\tBattleship\t{}\n'.format(battleship_sign1.rstrip(' '),battleship_sign2.rstrip(' ')))
        printer('Destroyer\t{}\t\t\t\tDestroyer\t{}\n'.format(sunken_ship('D',1,player1_board),sunken_ship('D',2,player2_board)))
        printer('Submarine\t{}\t\t\t\tSubmarine\t{}\n'.format(sunken_ship('S',1,player1_board),sunken_ship('S',2,player2_board)))
        printer('Patrol Boat\t{}\t\t\tPatrol Boat\t{}\n\n'.format(patrol_sign1.rstrip(' '),patrol_sign2.rstrip(' ')))
        
    if condition == False: # as long as there is no winner this block works
        round_count = round
        printer("{}'s Move\n\n".format(player))
        grid_size = 'Grid Size: 10x10\n\n'
        printer("Round : {}\t\t\t\t\t{}".format(round_count,grid_size))
        p1 = "Player1's Hidden Board"
        p2 = "Player2's Hidden Board\n"
        printer('{}\t\t{}'.format(p1,p2))
        boards()
        printer('Enter your move: {},{}\n'.format(*current_move))
        printer('\n')
    elif condition == True: # when there is one winner this block works
        printer(f'{player} Wins!\n\nFinal Information\n\n')
        p1 = "Player1's Board"
        p2 = "Player2's Board\n"
        printer("{}\t\t\t\t{}".format(p1,p2))
        boards()
    elif condition == 'Draw': # when both player wins this block works
        printer(f"It's a draw!\n\nFinal Information\n\n")
        p1 = 'Player1’s Board'
        p2 = 'Player2’s Board\n'
        printer("{}\t\t\t\t{}".format(p1,p2))
        boards()

def game_over_condition(playership): #checks if the players are out of ships to determine if the game is over
    total = 0
    for key in playership:
        total += playership[key]
    if total == 0:
        return True
        
try: # the code block for calling every function we need to use
    round = 1
    printer('Battle of Ships Game\n\n')
    for move in range(max(len(player1_moves),len(player2_moves))):
        try:
            current_move = [player1_moves[move][0]+1,lettervaluereverse[player1_moves[move][1]]] 
            print_grid(player1_empty_board,player2_empty_board,'Player1',False,round) #prints the first part of the round (player 1 turn)
            attack(player1_moves,player2_board,player2_empty_board,move)
        except IndexError:
            printer("Player 1's moves are over.\n")
            break
        all_sunk_ship_caller() #updates the ships after the first attack
        try:  
            current_move = [player2_moves[move][0]+1,lettervaluereverse[player2_moves[move][1]]]
            print_grid(player1_empty_board,player2_empty_board,'Player2',False,round) #prints the second part of the round (player 2 turn)
            attack(player2_moves,player1_board,player1_empty_board,move)
        except IndexError:
            printer("Player 2's moves are over.\n")
            break
        all_sunk_ship_caller() #updates the ships after the second attack
        if game_over_condition(player2_ships) and not game_over_condition(player1_ships): # breaks the loop if there is winning or draw condition
            print_grid(player1_board,player2_board,'Player1',True)
            break
        elif game_over_condition(player1_ships) and not game_over_condition(player2_ships):
            print_grid(player1_board,player2_board,'Player2',True)
            break
        elif game_over_condition(player1_ships) and game_over_condition(player2_ships):
            print_grid(player1_empty_board,player2_empty_board,'','Draw')
            break
        round += 1 
except:
    printer('kaBOOM: run for your life!')