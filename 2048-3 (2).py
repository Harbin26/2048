import sys
import logging


INPUT_FILE_PATH = "2048_in.txt"
TEST_CASE_LIST = []
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
log.addHandler(handler)
RESULT_LIST = []
ALLOWED_ACTIONS = ['L', 'R', "U", 'D']
MAX_SCORE = -sys.maxsize
ACTION_LIST = []


class Node:
    def __init__(self, value, name, level, parent):
        self.value = value
        self.name = name
        self.children = []
        self.level = level
        self.parent = parent

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.name) + "===" + repr(self.value) + "===" + repr(self.level) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret


def add_2_grid(input_array):
    """
       Gets the input array and returns a new modified array
       by adding 2 at the first empty spot on scanning vertically
    :return:
    """
    for i in range(4):
        for j in range(4):
            if input_array[i][j] == 0:
                input_array[i][j] = 2
                return


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


def bfs(root=None):
    """
    Perform bfs to search the best possible moves
    to get maximum score
    :param root:
    :return:
    """
    if root is None:
        return

    # score initially set to 0 and level is -1 , we track state by score and level
    queue = [[(0, -1), root]]
    max_score = -sys.maxsize
    path_node = None
    while len(queue) > 0:
        (score, level), cur_node = queue.pop(0)

        if level == 2:
            if score > max_score:
                max_score = score
                path_node = cur_node

            continue

        for children in cur_node.children:
            queue.append([(score + children.value, children.level), children])

    return max_score, path_node


def bfs_helper(input_grid, step, node):
    """
    Constructs the tree that is required for the bfs search.
    :param node:
    :param input_grid: Testcase input, single 2d array
    :param step: Number of random moves
    :param action_list: Action list
    :param score: possible scores from each move
    :return: Updates global variable ACTION_LIST
    """
    global MAX_SCORE, ACTION_LIST
    if step == 3:
        return

    new_grid = []
    for i in ALLOWED_ACTIONS:
        if i == 'L':
            step_score, new_grid = move_left(input_grid)
            temp_node = Node(step_score, 'L', step, node)
            node.children.append(temp_node)
            add_2_grid(new_grid)
        elif i == 'R':
            step_score, new_grid = move_right(input_grid)
            temp_node = Node(step_score, 'R', step, node)
            node.children.append(temp_node)
            add_2_grid(new_grid)
        elif i == 'U':
            step_score, new_grid = move_up(input_grid)
            temp_node = Node(step_score, 'U', step, node)
            node.children.append(temp_node)
            add_2_grid(new_grid)
        elif i == 'D':
            step_score, new_grid = move_down(input_grid)
            temp_node = Node(step_score, 'D', step, node)
            node.children.append(temp_node)
            add_2_grid(new_grid)

        bfs_helper(new_grid, step + 1, temp_node)


def get_path_string(node):
    """
        get comma seperated path String for solution
    :param node:
    :return:
    """

    if node is None:
        return ""

    cur_node = node
    path_str_list = []
    while cur_node.parent != None:
        path_str_list.append(cur_node.name)
        cur_node = cur_node.parent

    path_str_list.reverse()
    return path_str_list


def write_result_file():
    """
    Write the output to the 2048.out file
    :return:
    """
    global RESULT_LIST
    file_ptr = open('2048_out.txt', 'w')
    i = 1
    for ans in RESULT_LIST:
        if i == len(RESULT_LIST):
            file_ptr.write("{}".format(','.join(ans)))
        else:
            file_ptr.write("{}\n".format(','.join(ans)))
        i += 1
    file_ptr.close()


def get_test_case(test_case_input):
    """
       Read 4 lines of string and form a 2d grid
    :return: 2d test case array
    """

    test_case_array = []
    for i in test_case_input:
        temp_row = [int(item.strip()) for item in i.split(',')]
        test_case_array.append(temp_row)

    return test_case_array


def process_testcase(input_grid):
    """
     Process the test input to get the possible moves and
    :param input_grid: Input testcase, single 2d array
    :return:
    """
    global MAX_SCORE
    global ACTION_LIST
    MAX_SCORE = -sys.maxsize
    ACTION_LIST = []
    log.info("Test case processing %s", input_grid)
    root = Node(0, 'Root', -1, None)
    bfs_helper(input_grid, 0, root)
    max_score, path_node = bfs(root)
    path_string_list = get_path_string(path_node)
    RESULT_LIST.append([str(max_score)] + path_string_list)
    log.info("root view %s %s", str(max_score), path_string_list)


def process_testcases():
    """
    Process each testcases from the main testcase list.
    :return:
    """
    for test_case in TEST_CASE_LIST:
        process_testcase(test_case)

    log.info("Answer is %s", RESULT_LIST)

def read_input_file():
    """
        Read the input file and return the list with all the test case inputs
        indiviual testcases are 2d grid
    :return:
    """
    file_ptr = open(INPUT_FILE_PATH, 'r')
    all_lines = file_ptr.readlines()
    test_cases = int(all_lines[0])
    total_lines = 4 * test_cases

    # move in interval of number of test case
    test_case_num = 1
    while test_case_num < total_lines:
        test_case_inp = get_test_case(all_lines[test_case_num:test_case_num + 4])
        TEST_CASE_LIST.append(test_case_inp)
        test_case_num += 4


def main():
    read_input_file()
    log.info("Input array: %s", TEST_CASE_LIST)
    process_testcases()
    write_result_file()


if __name__ == "__main__":
    main()
