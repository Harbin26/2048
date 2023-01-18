import copy
import sys
import logging
import random

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
log.addHandler(handler)
RESULT_LIST = []
ALLOWED_ACTIONS = ['L', 'R', "U", 'D']
MAX_SCORE = -sys.maxsize
ACTION_LIST = []
N = 100



def is_2048_game(mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 2048:
                return True

    return False


def game_end(mat):
    """
        game is end when either 2048 is reached or no more vacant places.
    :param matrix:
    :return:
    """
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 2048:
                return True

        # if we are still left with
    # atleast one empty cell , game is not over
    for i in range(4):
        for j in range(4):
            if (mat[i][j] == 0):
                return False

    for i in range(3):
        for j in range(3):
            if (mat[i][j] == mat[i + 1][j] or mat[i][j] == mat[i][j + 1]):
                return False

    for j in range(3):
        if (mat[3][j] == mat[3][j + 1]):
            return False

    for i in range(3):
        if (mat[i][3] == mat[i + 1][3]):
            return False

    return True


def add_2_or_4_grid(input_array, input_value):
    """
        This function should be called only if valid values are found
    :return:
    """
    r = random.randint(0, 3)
    c = random.randint(0, 3)
    random_generated_set = set()
    while input_array[r][c] != 0:
        r = random.randint(0, 3)
        c = random.randint(0, 3)

    input_array[r][c] = input_value

    return input_array


def randomly_generate_2_4():
    return random.choice([2, 4])


def move_elements_left(input_array):
    """
     Move the elements to left's occupying the empty spots. This operations fills up the empty spot if found any
      on left movement
    :param input_array:
    :return: action performed array, grid changed status
    """
    new_array = [[0, 0, 0, 0] for i in range(4)]
    is_grid_changed = True
    for i in range(4):
        last_zero_ptr = 0
        for j in range(4):
            if input_array[i][j] != 0:
                new_array[i][last_zero_ptr] = input_array[i][j]
                last_zero_ptr += 1
                if j != last_zero_ptr:
                    is_grid_changed = True

    return [new_array, is_grid_changed]


def combine_input_grid(input_array):
    """
        Combine grid and return the total sum of the array
        function scans for the adjacent elements with same value and combine them to one value to the left.
        it calculates sum of all the merges.
    :param input_array: Input 2d grid
    :return:
    """
    total_sum = 0
    for i in range(4):
        for j in range(3):
            if input_array[i][j] == input_array[i][j + 1]:
                input_array[i][j] = input_array[i][j] * 2
                input_array[i][j + 1] = 0
                total_sum += input_array[i][j]

    log.debug("After Combining input Grid %s", input_array)
    return total_sum, input_array


def transpose(input_array):
    """
    Transpose the matrix
    :param input_array: Input 2d grid
    :return: Transposed matrix
    """
    new_matrix = []
    for i in range(4):
        new_matrix.append([])
        for j in range(4):
            new_matrix[i].append(input_array[j][i])
    return new_matrix


def reverse_input_grid(input_array):
    """
    Reverse the matrix
    :param input_array: Input
    :return:
    """
    new_matrix = []
    for i in range(4):
        new_matrix.append(input_array[i][::-1])

    return new_matrix


def move_left(input_array):
    """
        Move the grids to the left as 2048 action

        Algorithm: move all the elements to left
        combine the same numbers adjacent by left and move all the elements to left again
    :param input_array: Input 2d grid
    :return: Total sum from the action, changed grid
    """

    new_array, changed = move_elements_left(input_array)
    log.debug("After moving left -- %s", new_array)
    [total_sum, new_grid] = combine_input_grid(new_array)
    new_input_grid, is_grid_changed = move_elements_left(new_grid)
    return [total_sum, new_input_grid]


def move_right(input_array):
    """
    Reverse all the elements, merge same elements and move the elements to left and reverse again.
    :param input_array: Input 2d grid
    :return: Total sum from the action, changed grid
    """
    rever_array = reverse_input_grid(input_array)
    total_sum, new_grid = move_left(rever_array)
    original_grid = reverse_input_grid(new_grid)
    return [total_sum, original_grid]


def move_up(input_array):
    """
    :param input_array: Input 2d grid
    :return: Total sum from the action, changed grid
    """
    transpose_array = transpose(input_array)
    total_sum, modified_grid = move_left(transpose_array)
    original_grid = transpose(modified_grid)
    return [total_sum, original_grid]


def move_down(input_array):
    """
    Transpose and move the elements to right and transpose again
    to get the move down operation
    :param input_array: Input 2d grid
    :return: Total sum from the action, changed grid
    """
    transpose_array = transpose(input_array)
    total_sum, modified_grid = move_right(transpose_array)
    original_grid = transpose(modified_grid)
    return [total_sum, original_grid]


def move_action(action, matrix):
    """

    :param action:
    :param state:
    :return:
    """
    log.debug("Matrix before taking action %s", matrix)
    if action == 'L':
        score, state = move_left(matrix)

    if action == 'R':
        score, state = move_right(matrix)

    if action == 'U':
        score, state = move_up(matrix)

    if action == 'D':
        score, state = move_down(matrix)

    return score, state


def generete_random_initial_board():
    matrix = []
    for i in range(4):
        matrix.append([0] * 4)

    matrix = add_2_or_4_grid(matrix, 2)
    matrix = add_2_or_4_grid(matrix, 2)
    return matrix


def generate_all_states(state, empty_locations_list):

    state_list = []
    for i, j in empty_locations_list:
        state_list.append(add_value_index(state, 2, i, j))
        state_list.append(add_value_index(state, 4, i, j))

    return state_list


def check_score_exist(state):
    """

    :param state:
    :return:
    """
    score_exist = False
    for action in ALLOWED_ACTIONS:
        t_score, new_state = move_action(action, state)
        if t_score != 0:
            score_exist = True
            break;

    return score_exist


def get_index_of_empty_loc(matrix):

    list_of_index = []
    for i in range(4):
        for j in range(4):
            if matrix[i][j] == 0:
                list_of_index.append((i,j))

    return list_of_index

def check_next_score_available(state):
    """

    :param state:
    :return:
    """
    list_of_empty_locations = get_index_of_empty_loc(state)
    list_of_states = generate_all_states(state, list_of_empty_locations)
    score_available = False
    for temp_state in list_of_states:
        score_available = check_score_exist(temp_state)
        if score_available:
            break

    return score_available

def add_value_index(matrix, value, row, col):

    new_state = copy.deepcopy(matrix)
    new_state[row][col] = value
    return new_state

def generate_current_score_data(matrix):
    current_score_list = []
    for action in ALLOWED_ACTIONS:
        score, state = move_action(action, matrix)
        if score != 0:
            current_score_list.append((score, action, state))

    return current_score_list


def generate_random_next_state(current_score_list, state):
    """

    :param current_score_list:
    :param state:
    :return:
    """
    last_move = None
    if len(current_score_list) == 0:
        last_move = ALLOWED_ACTIONS[random.randint(0, 3)]
        score, l_state = move_action(last_move, state)
        return score, last_move, add_2_or_4_grid(l_state, randomly_generate_2_4())

    selection_list = []
    for score, last_move, state in current_score_list:
        next_score = check_next_score_available(state)
        if next_score:
            selection_list.append((score, last_move, state))

    if len(selection_list) == 0:
        score, last_move, l_state = current_score_list[random.randint(0, len(current_score_list)-1)]
        return score, last_move, add_2_or_4_grid(l_state, randomly_generate_2_4())

    score, last_move, l_state = random.choice(selection_list)
    return score, last_move, add_2_or_4_grid(l_state, randomly_generate_2_4())


def play_2048_game():
    """

    :return:
    """
    matrix = generete_random_initial_board()
    log.debug("Empty board %s", matrix)

    game_moves = []
    state = copy.deepcopy(matrix)
    total_score = 0
    while True:
        if game_end(state):
            break

        current_score_list = generate_current_score_data(state)
        score, last_move, state = generate_random_next_state(current_score_list, state)
        total_score += score
        game_moves.append(last_move)

    # once the game ends , push the end state, initial state list of
    return [total_score, matrix, state, game_moves]


def simulate_random_search():
    """
    Process each testcases from the main testcase list.
    :return:
    """

    game_count = 1
    max_score = 0
    first_state = None
    last_state = None
    actions = None
    while game_count <= N:
        score, initial_state, end_state, game_moves = play_2048_game()
        if is_2048_game(end_state):
            max_score = score
            first_state = initial_state
            last_state = end_state
            actions = game_moves
            break

        elif score >= max_score:
            max_score = score
            first_state = initial_state
            last_state = end_state
            actions = game_moves
        game_count += 1

    print("Total Games Played", str(N))

    print("Game with Max Score Details \n")

    print("Initial State \n")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in first_state]))

    print("\nTotal Score of the Game %s \n" % str(max_score))

    print("List of Actions %s \n" % str(actions))

    print("Final State of the Game \n")
    print('\n'.join(['\t'.join(['{:4}'.format(str(cell)) for cell in row]) for row in last_state]))



def main():
    simulate_random_search()


if __name__ == "__main__":
    main()
