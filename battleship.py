# First try of creating skeletons of game functions

# ---- MENU, GENERAL SETTINGS OF GAME AND GAME'S ENGINES ----
import string
from os import system, name
from time import sleep
import random

def clear_console():
    """Clears console."""
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")


def main_menu():
    """Services menu with game options"""
    GAME_MODES = {"1": "hot_seat", "2": "AI"}
    MAP_SIZES = (5,6,7,8,9,10)
    print("Welcome in\nBATTLESHIPS\n")
    
    usr_mode = choose_game_mode(GAME_MODES)
    usr_map_size = choose_map_size(MAP_SIZES)
    usr_turns_limit = specify_turns_limit()
    print(usr_mode)
    if GAME_MODES[usr_mode] == "hot_seat":
        start_game((usr_map_size, usr_map_size), turns_limit=usr_turns_limit, AI=False)
    else:
        start_game((usr_map_size, usr_map_size), turns_limit=usr_turns_limit, AI=True)


def choose_game_mode(available_game_modes):
    """Gets choice of game mode hot-seat or single-player(with AI)"""
    usr_game_mode_choice = ""
    
    choice_is_not_valid = lambda usr_game_mode_choice: usr_game_mode_choice not in available_game_modes.keys()
    
    print("Pick game mode from: 1. HOTSEAT 2. P VS AI (in progess)")
    while choice_is_not_valid(usr_game_mode_choice):
        usr_game_mode_choice = input("Your pick: ")
        if choice_is_not_valid(usr_game_mode_choice):
            print("Invalid choice.")

    return usr_game_mode_choice


def choose_map_size(available_map_sizes):
    """Gets validated choice of map size"""
    usr_map_size_choice = ""
    
    choice_is_not_valid = lambda map_size_choice: map_size_choice not in available_map_sizes
    
    print("Pick map size from pool 5-10.")
    while choice_is_not_valid(usr_map_size_choice):
        usr_map_size_choice = int(input("Your pick: "))
        if choice_is_not_valid(usr_map_size_choice):
            print("Invalid choice.")

    return usr_map_size_choice


def specify_turns_limit():
    """Get's user choice of turns limit or unlimited (returns None) if no input."""
    try:
        usr_turns_choice = int(input("Specify turns limit (10-30), or leave blank to set no limit: "))
        
        while usr_turns_choice > 30 or usr_turns_choice < 3:
            print("Incorrect choice. Choose from 10-30")
            usr_turns_choice = int(input("Try again: "))
        
        return usr_turns_choice

    except ValueError:
        return None


def show_turns_left(turns_left):
    """Prints current state of turns_left if turns_left is not None. If it is, print 'Unlimited'."""
    print(f"Turns left: {turns_left}")


def start_game(maps_size, turns_limit=None, AI=False):
    """Processes one whole hotseat game"""
    global ROWS, COLS, BOARD_LENGTH, BOARD_WIDTH
    BOARD_LENGTH, BOARD_WIDTH = maps_size
    ROWS, COLS = create_coordinates_translation_dictionary(BOARD_LENGTH, BOARD_WIDTH)
    
    player1_board = init_board(length=BOARD_LENGTH, width=BOARD_WIDTH)
    player1_hidden_board = init_board(length=BOARD_LENGTH, width=BOARD_WIDTH)
    player1_ships = []

    player2_board = init_board(length=BOARD_LENGTH, width=BOARD_WIDTH)
    player2_hidden_board = init_board(length=BOARD_LENGTH, width=BOARD_WIDTH)
    player2_ships = []
    
    service_placing_phase(player1_board, player2_board, [3, 2, 2], player1_ships, player2_ships, AI)
    has_p1_won = has_won(player2_ships)
    has_p2_won = has_won(player1_ships)
    
    if turns_limit != None:
        turns_left = turns_limit

    while not (has_p1_won or has_p2_won):
        print("Player 1 turn")
        if turns_limit != None:
            show_turns_left(turns_left)
        
        process_turn_of_player(player1_board, player2_hidden_board, player2_board, player2_ships, AI=AI)
        has_p1_won = has_won(player2_ships)
    
        if has_p1_won:
            continue
        
        print("Player 2 Turn")
        if turns_limit != None:
            show_turns_left(turns_left)
        
        process_turn_of_player(player2_board, player1_hidden_board, player1_board, player1_ships)
        has_p2_won = has_won(player1_ships)
        
        if turns_limit != None:
            turns_left -= 1
            if turns_left == 0:
                break

    if has_p1_won:
        return finish_game("Player 1")
    elif has_p2_won:
        return finish_game("Player 2")
    else:
        return finish_game("NONE")
    

# ---- BOARD ----

def init_board(length=5, width=5):
    """Initialize board of given size. By default 5x5."""
    board = []

    for i in range(length):
        board.append(["0"] * width)
    
    return board


def print_board_of_player(player_board):
    """Print board for given player."""
    
    print("".ljust(4) + " ".join([str(number) for number in range(1, BOARD_WIDTH+1)]) + "\n")
    
    for row_number, row in enumerate(player_board):
        print(string.ascii_uppercase[row_number].ljust(3) + " " + " ".join(row))


def create_coordinates_translation_dictionary(board_length, board_width):
    """Returns two dictionaries based on board width and length for input translation purposes"""
    letters = string.ascii_uppercase
    rows_dictionary = dict()
    columns_dictionary = dict()
    
    for length_number in range(board_length):
        rows_dictionary[letters[length_number]] = length_number
    
    for width_number in range(board_width):
        columns_dictionary[str(width_number+1)] = width_number
    
    return rows_dictionary, columns_dictionary


# --- PLACING PHASE ---

def service_placing_of_player(player_board, ships_lengths_list, player_ships, AI = False):
    """Services placing phase of given human or AI player. 
    After this function all ships of player are placed."""    
    for ship_length in ships_lengths_list:
        print_board_of_player(player_board)
        print(f"Placing ship with length: {ship_length}.")
        
        is_hot_seat_game = AI == False
        
        if is_hot_seat_game:
            coord1, coord2  = get_single_coordinate(), get_single_coordinate()
            user_coords = translate_user_coords(coord1), translate_user_coords(coord2)
            while not is_user_placing_correct(ship_length, player_board, user_coords):
                print("Incorrect coords.")
                coord1, coord2  = get_single_coordinate(), get_single_coordinate()
                user_coords = translate_user_coords(coord1), translate_user_coords(coord2)
        
        else:
            user_coords = placing_ai_wrapper(player_board, ship_length)

        place_single_ship(ship_length, player_board, player_ships, user_coords)
        if AI == True:
            sleep(2)
        clear_console()


def service_placing_phase(p1_board, p2_board, ships_lengths_list, p1_ships, p2_ships, AI=False):
    """Service placing phase of both players. After one's player placing phase is finished
    program gives information about this fact and waits for pressing any key to continue."""
    service_placing_of_player(p1_board, ships_lengths_list, p1_ships, AI=AI)
    print_board_of_player(p1_board)
    
    input("Press enter to start placing of second player... ")
    clear_console()
    
    service_placing_of_player(p2_board, ships_lengths_list, p2_ships)
    print_board_of_player(p2_board)

    input("All ships placed. Press enter to begin the battle... ")
    clear_console()

# --- HUMAN PLACING ---

def get_single_coordinate():
    """Gets single, validated coordinate of player. In this version 'A-J1-10' supported.""" 
    correct_ROWS = ROWS.keys()
    correct_COLS = COLS.keys()
    
    
    user_input = str.upper(input("Your coordinate:"))
    
    input_length_not_correct = len(user_input) < 2 or len(user_input) > 3 
    while input_length_not_correct:
        print("Incorrect input.")
        user_input = str.upper(input("Try again: "))     
        input_length_not_correct = len(user_input) < 2 or len(user_input) > 3

    input_is_not_correct = user_input[0] not in correct_ROWS or user_input[1:] not in correct_COLS
    while input_is_not_correct:
        print("Incorrect input.")
        user_input = str.upper(input("Try again: "))
        input_is_not_correct = user_input[0] not in correct_ROWS or user_input[1:] not in correct_COLS

    return user_input


def translate_user_coords(coordinate):
    """Translate eg. (A4) coords for int type coords (0,5)"""
    row1, col1 = ROWS[coordinate[0]], COLS[coordinate[1:]]
    coords = (row1,col1)
    
    return coords

# PLACING PHASE AI

def get_empty_fields(player_board):
    """Get empty fields of player board. Help function for AI placing"""
    empty_fields_list = []
    for row_index in range(len(player_board)):
        for col_index in range(len(player_board[0])):
            if player_board[row_index][col_index] == "0":
                empty_fields_list.append((row_index,col_index))
    return empty_fields_list
    

def get_placing_ai(player_board, ship_length):
    """Returns random placing coords in correct order. Help function for AI placing."""
    empty_fields = get_empty_fields(player_board)
    
    row1, col1 = random.choice(empty_fields)
    row_or_col = random.choice(["row", "col"])

    if row_or_col == "row":
        modified_field = col1
        
        if modified_field + ship_length - 1 > len(player_board[0]) - 1:
            modified_field -= ship_length - 1
        
        elif modified_field - ship_length + 1 < 0:
            modified_field += ship_length - 1
        
        else:
            modified_field += ship_length - 1
        
        if col1 < modified_field:
            return (row1, col1), (row1, modified_field)
        
        else:
            return (row1, modified_field), (row1, col1)
    
    else:
        modified_field = row1
        
        if modified_field + ship_length - 1 > len(player_board[0]) - 1:
            modified_field -= ship_length - 1
        
        elif modified_field - ship_length + 1 < 0:
            modified_field += ship_length - 1
        
        else:
            modified_field += ship_length - 1
        
        if row1 < modified_field:
            return (row1, col1), (modified_field, col1)
        
        else:
            return (modified_field, col1), (row1, col1)
    

def placing_ai_wrapper(player_board, ship_length):
    """Wrapper function for AI placing. Infinitely get random placing coords until they are correct and then returns them"""
    while True:
        placing_coords_ai = get_placing_ai(player_board, ship_length)
        if is_user_placing_correct(ship_length, player_board, placing_coords_ai):
            return placing_coords_ai 

# --- GENERAL PLACING ---

def get_upper_row(player_board, coords, ship_length):
    """Upper part of get_neighbour_fields"""
    row1, col1 = coords[0][0], coords[0][1]
    row2, col2 = coords[1][0], coords[1][1]
    min_col = min(col1,col2)
    if max(row1,row2) == len(player_board)-1:
        return []
    elif col1 == col2:
        return [player_board[max(row1,row2)+1][col1]] 
    else:
        return player_board[max(row1,row2)+1][min_col:min_col+ship_length]


def get_lower_row(player_board, coords, ship_length):
    """Lower part of get_neighbour_fields"""
    row1, col1 = coords[0][0], coords[0][1]
    row2, col2 = coords[1][0], coords[1][1]
    min_col = min(col1,col2)

    if min(row1,row2) == 0:
        return []
    elif col1 == col2:
        return [player_board[min(row1,row2)-1][col1]] 
    else:
        return player_board[min(row1,row2)-1][min_col:min_col+ship_length]


def get_left_column(player_board, coords, ship_length):
    """Left part of get_neighbour_fields"""
    row1, col1 = coords[0][0], coords[0][1]
    row2, col2 = coords[1][0], coords[1][1]
    min_row = min(row1,row2)
    if min(col1,col2) == 0:
        return []
    elif row1 == row2:
        return [player_board[row1][min(col1,col2)-1]] 
    else:
        return [player_board[min_row + counter][min(col1,col2)-1] for counter in range(0,ship_length)]


def get_right_column(player_board, coords, ship_length):
    """Right part of get_neighbour_fields"""
    row1, col1 = coords[0][0], coords[0][1]
    row2, col2 = coords[1][0], coords[1][1]
    min_row = min(row1,row2)
    if max(col1,col2) == len(player_board[0])-1:
        return []
    elif row1 == row2:
        return [player_board[row1][max(col1,col2)+1]] 
    else:
        return [player_board[min_row + counter][max(col1,col2)+1] for counter in range(0,ship_length)]


def get_neighbour_fields(player_board, coordinates, ship_length):
    """Return list of states of neighbour fields of ships of given length on given coords."""
    upper_row = get_upper_row(player_board, coordinates, ship_length)
    lower_row = get_lower_row(player_board, coordinates, ship_length)
    left_column = get_left_column(player_board, coordinates, ship_length)
    right_column = get_right_column(player_board, coordinates, ship_length)
    
    return upper_row + lower_row + left_column + right_column


def is_user_placing_correct(ship_length, player_board, user_coordinates):
    """Return True if user input is in right scope e.g. (A1, c1) and 
place is free or False if it's not correct or not free e.g. (a1, c3), (C5,G20) etc."""
    coordinate1, coordinate2 = user_coordinates
    
    row1, col1 = coordinate1[0], coordinate1[1]
    row2, col2 = coordinate2[0], coordinate2[1]
    
    move_is_in_row = row1 == row2
    move_is_in_col = col1 == col2
    is_ship_out_of_board = lambda direction, coord1, coord2: min(coord1, coord2) + ship_length-1 not in direction.values() 
    neighbour_fields = get_neighbour_fields(player_board, ((row1, col1), (row2, col2)), ship_length)

    if not move_is_in_row and not move_is_in_col:
        return False
    
    elif "X" in neighbour_fields:
        return False

    if move_is_in_row:
        taken_areas_list = [state_of_area for state_of_area in player_board[row1][col1:col2]]
        if is_ship_out_of_board(COLS, col1, col2):
            return False
    
    elif move_is_in_col:
        taken_areas_list = [player_board[row_number][col1] for row_number in range(row1, row2)]
        if is_ship_out_of_board(ROWS, row1, row2):
            return False


    return True if taken_areas_list.count("0") == len(taken_areas_list) else False  


def place_single_ship(ship_length, player_board, player_ships, ships_coords):
    """Marking correct fields on board as ship."""
    row1, col1 = ships_coords[0][0], ships_coords[0][1]
    row2, col2 = ships_coords[1][0], ships_coords[1][1]
    
    ship_placing_counter = 0
    row_counter = min(row1, row2)
    col_counter = min(col1, col2)
    
    ship_coordinates_list = []
    
    while ship_placing_counter < ship_length:
        
        if col1 == col2:
            player_board[row_counter][col1] = "X"
            ship_coordinates_list.append([row_counter, col1, "X"])
            if row1 < row2:
                row_counter += 1
            else:
                row_counter -= 1
        else:
            player_board[row1][col_counter] = "X"
            ship_coordinates_list.append([row1, col_counter, "X"])
            if col1 < col2:
                col_counter += 1
            else:
                col_counter -= 1
    
        ship_placing_counter +=1

    player_ships.append(ship_coordinates_list)


# ---- SHOOTING PHASE ----

def process_turn_of_player(players_board, copy_of_opp_board, opponent_board, opponent_ships, AI=False):
    """Service one full turn of player, consistning while-looped getting coordinates to shot, 
displaying feedback and checking for win until miss. """
    shot_result = ""
    while shot_result != "M":
        
        print("Your board:") 
        print_board_of_player(players_board)
        
        print("Your copy of opponent board:") 
        print_board_of_player(copy_of_opp_board)
        
        if AI == False:
            player_shot = get_single_coordinate()
            shotted_row_index, shotted_col_index = translate_user_coords(player_shot)
        
        else:
            player_shot = get_ai_shot_coord(copy_of_opp_board, opponent_ships)
            shotted_row_index, shotted_col_index = player_shot[0], player_shot[1]
        
        shot_result = process_a_shot(shotted_row_index, shotted_col_index, copy_of_opp_board, opponent_board, opponent_ships)
        
        display_feedback_after_shot(shot_result)
        sleep(2)
        clear_console()
        if has_won(opponent_ships):
            return None


def process_a_shot(shot_row, shot_col, players_copy_of_opp_board, opponent_board, opponent_ships):
    """Serve whole process of shot for given (shot_row, shot_col) and changes state of field on both of boards"""
    state_of_shotted_field = opponent_board[shot_row][shot_col]
    
    if state_of_shotted_field == "0":
        
        if players_copy_of_opp_board[shot_row][shot_col] == "M":
            shot_result = "M_repeat"
            return shot_result
        
        shot_result = "M"
        mark_shot_on_board(shot_row, shot_col, players_copy_of_opp_board, shot_result)
    
    elif state_of_shotted_field == "X":
        shot_result = "H"
        mark_shot_on_board(shot_row, shot_col, players_copy_of_opp_board, shot_result)
        update_ships_state(shot_row, shot_col, opponent_ships, players_copy_of_opp_board, opponent_board)

        if is_ship_sunk(shot_row, shot_col, opponent_ships):
            shot_result = "S"
    

    return shot_result
    

def mark_shot_on_board(row_index, col_index, board, shot_result):
    """Mark shot with given shot result on given board."""
    board[row_index][col_index] = shot_result


def drown_ship_on_board(players_copy_board, opponent_board, players_ship, ship_num):
    """Changes state for sunk ("S") of ship with all parts hit on both of boards"""
    for part in players_ship[ship_num]:
        mark_shot_on_board(part[0], part[1], players_copy_board, "S")
        mark_shot_on_board(part[0], part[1], opponent_board, "S")


def update_ships_state(row_index, column_index, players_ships, players_copy_board, opponent_board):
    """Update state of ships. It contains changing ships state for sunk."""
    for ship_num in range(len(players_ships)):
        for row, col, state in players_ships[ship_num]:
            
            if row_index == row and column_index == col:
                players_ships [ship_num] [players_ships[ship_num].index([row, col, state])] [2] = "H"
        
        states_of_ship = [part[2] for part in players_ships[ship_num]]
        all_ships_part_hit = "X" not in states_of_ship
        
        if all_ships_part_hit:
            ship = [[part[0], part[1], "S"] for part in players_ships[ship_num]]
            players_ships[ship_num] = ship
            drown_ship_on_board(players_copy_board, opponent_board, players_ships, ship_num)


def is_ship_sunk(row_index, column_index, players_ships):
    """Checks if ship which contain part of given coords is sunk."""
    for ship in players_ships:
        for part in ship:
            if part[0] == row_index and part[1] == column_index and part[2] == "S":
                return True
    return False


def display_feedback_after_shot(result_of_shot):
    """Display adequate communicate after shot made on given coordinates."""
    if result_of_shot == "H":
        print("You hitted the ship. Try to hit next one!")
    elif result_of_shot == "M":
        print("You missed.")
    elif result_of_shot == "S":
        print("You've sunk enemy ship.")
    elif result_of_shot == "M_repeat":
        print("You have tryed this already! Try other coords!")


# SHOOTING PHASE AI

def get_hit_fields(opponent_ships):
    """Get coords of already hit fields. Help function for AI shooting."""
    hit_fields_coords_list = []
    
    for ship in opponent_ships:
        for part in ship:
            if part[2] == "H":
                hit_fields_coords_list.append((part[0], part[1]))
    
    return hit_fields_coords_list


def get_neighs_of_shot(hit, copy_of_opp_board):
    """Get neighbour coords for given hit coords. Help function for AI shooting."""
    upper = (hit[0]+1, hit[1]) if hit[0]+1 < len(copy_of_opp_board) else None
    right = (hit[0], hit[1]+1) if hit[1]+1 < len(copy_of_opp_board[0]) else None
    lower = (hit[0]-1, hit[1]) if hit[0]-1 >= 0 else None
    left = (hit[0], hit[1]-1) if hit[1]-1 >= 0 else None
    
    return lower, right, upper, left


def get_ai_shot_coord(copy_of_opp_board, opponent_ships):
    """Wrapper for AI shooting. Gets list of already hit fields, if its empty returns random shot. 
    If its not iterates over hit fields and over its neighbours in purpose to get another succesful shots.
    It does not check neighbours which are neighbours for sunk ships ("S"), as they cannot contain another ship's parts"""
    hit_fields = get_hit_fields(opponent_ships)
    
    if len(hit_fields) == 0:
        return random.choice(get_empty_fields(copy_of_opp_board))
    
    for hit in hit_fields:
        neighs = get_neighs_of_shot(hit, copy_of_opp_board)
        for neigh in neighs:
            if neigh != None:
                row, col = neigh[0], neigh[1]
                if copy_of_opp_board[row][col] == "0" and "S" not in get_neighbour_fields(copy_of_opp_board, ((row,col), (row, col)), 1):
                    return neigh


# --- Win checker and game finishing functions ---

def has_won(opponent_ships):
    """Returns True if given player have shoot all opponent's ships, else False"""
    return "X" not in [ship[part][2] for ship in opponent_ships for part in range(len(ship))]


def greet_player_after_won(player):
    """Prints winning message for winning player"""
    player_string_length = len(player)
    print(f"""
    {"=" * player_string_length}
    {player}
    {"=" * player_string_length}
    {" " * (player_string_length-7)}has won
    """)


def finish_game(player):
    """Thanks players for the game and asks for the next try"""
    greet_player_after_won(player)
    print("Do you want to try again?")
    user_decision = input("y/n : ")
    if str.lower(user_decision) == "y":
        return True
    else:
        return False


if "__main__" == __name__:    
    #main_menu()
    start_game((5,5), AI=True)