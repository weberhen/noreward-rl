import cv2
import numpy as np

def draw_case(x, y, color, board):
    board[y * case_size:(y + 1) * case_size, x * case_size:(x + 1) * case_size] = color
    return board

def draw_q_value_on_board(q_table, board):
    for i in range(rows):
        for j in range(cols):
            # board = cv2.putText(board, str(int(q_table[j, i])), (j * case_size, i * case_size), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (255, 255, 255), 1)
            # paint the board in grayscale using the q value
            if q_table[j,i] < 0:
                color = [0, 0, abs(q_table[j,i])*10]
            else:
                color = [0, min(255,abs(q_table[j,i])), 0]
            board = draw_case(j, i, color, board)
    return board

def get_potential_moves(curr_pos, rows, cols):
    # curr_pos is a tuple of (x, y)
    # returns a list of tuples of (x, y)
    # where x and y are the potential moves
    # that the piece can make
    potential_moves = []
    # to the left
    if curr_pos[0] > 0:
        potential_moves.append((curr_pos[0] - 1, curr_pos[1]))
    # to the right
    if curr_pos[0] < cols - 1:
        potential_moves.append((curr_pos[0] + 1, curr_pos[1]))
    # down
    if curr_pos[1] < rows - 1:
        potential_moves.append((curr_pos[0], curr_pos[1] + 1))
    # up
    if curr_pos[1] > 0:
        potential_moves.append((curr_pos[0], curr_pos[1] - 1))
    # diagonal moves
    if curr_pos[0] > 0 and curr_pos[1] > 0:
        potential_moves.append((curr_pos[0] - 1, curr_pos[1] - 1))
    if curr_pos[0] < cols - 1 and curr_pos[1] > 0:
        potential_moves.append((curr_pos[0] + 1, curr_pos[1] - 1))
    if curr_pos[0] > 0 and curr_pos[1] < rows - 1:
        potential_moves.append((curr_pos[0] - 1, curr_pos[1] + 1))
    if curr_pos[0] < cols - 1 and curr_pos[1] < rows - 1:
        potential_moves.append((curr_pos[0] + 1, curr_pos[1] + 1))
    return potential_moves
    

def transform_to_index(pos, cols):
    # pos is a tuple of (x, y)
    # returns the index of the position
    # in the flattened board
    return pos[1] * cols + pos[0]



case_size = 20
rows = 20
cols = 20
num_elements = rows * cols
# q_table = np.zeros((num_elements, num_elements))
# r_table = np.zeros((num_elements, num_elements)) 
q_table = np.zeros((cols, rows))

# # add 1 too all elements to the left of a given position
# for i in range(1,num_elements):
#     if i % cols != 0:
#         r_table[i - 1][i] = 0

# # add 1 too all elements to the right of a given position
# for i in range(num_elements):
#     if i % cols != cols - 1:
#         r_table[i + 1][i] = 0

# curr_pos = [0, 0]
goal_pos = [0, 5]
q_table[goal_pos[0], goal_pos[1]] = 100
# make a wall of -1 in the middle of the board

first_pos = True
episode = 0
skip_episodes = 1000
queue = []
while True:
    if first_pos:
        curr_pos = [np.random.randint(0, cols), np.random.randint(0, rows)]
        first_pos = False
        for i in range(0, 10):
            q_table[i, 7] = -10
        # another wall but vertical, from the bottom to the half of the board
        for i in range(15, rows-2):
            q_table[10, i] = -10
        # another wall but vertical, from the top to the half of the board
        for i in range(2,15):
            q_table[10, i] = -10
    # clear board
    if episode%skip_episodes == 0:
        board = np.zeros((rows * case_size, cols * case_size, 3), dtype=np.uint8)
        board = draw_q_value_on_board(q_table, board)
    potential_moves = get_potential_moves(curr_pos, rows, cols)
    potential_moves_indices = [transform_to_index(move, cols) for move in potential_moves]
    # pick a random move between the ones with the highest q value
    # get values of potential moves from q table
    potential_moves_values = [q_table[move[0], move[1]] for move in potential_moves]
    # pick all moves with the highest value
    max_value = max(potential_moves_values)
    # pick the best move
    next_move_index = np.random.choice([i for i, j in enumerate(potential_moves_values) if j == max_value])
    next_pos = list(potential_moves[next_move_index])
    ############################
    # if new position have never been visited, mark it as -1 
    if q_table[next_pos[0], next_pos[1]] <= 0:
        q_table[curr_pos[0], curr_pos[1]] -= 1
    # if next_pos is more than zero, give current position a reward of 1
    if q_table[next_pos[0], next_pos[1]] > 0:
            q_table[curr_pos[0], curr_pos[1]] += 1
    if next_pos == goal_pos:
        q_table[curr_pos[0], curr_pos[1]] += 1
    ############################

    if episode%skip_episodes == 0:
        board = draw_case(curr_pos[0], curr_pos[1], (0, 0, 255), board)
        board = draw_case(next_pos[0], next_pos[1], (0, 255, 0), board)
    curr_pos = next_pos
    if curr_pos == goal_pos:
        q_table[curr_pos[0], curr_pos[1]] += 1
        curr_pos = [0, 0]
        first_pos = True
        # reset all values below 0
        q_table[q_table < 0] = 0
        print("episode: ", episode)
        episode += 1
        queue = []
    if episode%skip_episodes == 0:
        cv2.imshow('board', board)
        cv2.waitKey(1)
    queue.append(curr_pos)
cv2.imshow('board', board)
cv2.waitKey(0)