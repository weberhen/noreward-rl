import cv2
import numpy as np

class Agent:
    def __init__(self, x, y, agent_color=(0, 0, 255)):
        self.x = x
        self.y = y
        self.moves = 0
        self.agent_color = agent_color

    def reached_goal(self, goal):
        return self.x == goal[0] and self.y == goal[1]

    def move(self, x, y):
        self.x = x
        self.y = y
        self.moves += 1

class MazeGame:
    def __init__(self, case_size=20, rows=20, cols=20) -> None:
        self.case_size = case_size
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows * case_size, cols * case_size, 3), np.uint8)
        self.goal_pos = (cols - 1, rows - 1)
        self.goal_color = [0, 255, 0]
        self.walls_color = [100, 100, 100]
        self.draw_case(self.goal_pos[0], self.goal_pos[1], self.goal_color)
        self.walls = []
        self.create_walls(100)

    def draw_case(self, x, y, color):
        self.board[y * self.case_size:(y + 1) * self.case_size, x * self.case_size:(x + 1) * self.case_size] = color

    def create_walls(self, num_walls, agents_pos=[]):
        # fix random seed to get the same maze every time
        np.random.seed(2)
        # create random walls
        for i in range(num_walls):
            x = np.random.randint(0, self.cols)
            y = np.random.randint(0, self.rows)
            if (x, y) not in self.walls and (x, y) != self.goal_pos and (x, y) != agents_pos:
                self.walls.append((x, y))

    def draw_walls(self):
        for wall in self.walls:
            self.draw_case(wall[0], wall[1], self.walls_color)

    def display(self, agents_pos=[], agents_colors=[]):
        # clear the board
        self.board = np.zeros((self.rows * self.case_size, self.cols * self.case_size, 3), np.uint8)
        # draw the agents
        for i in range(len(agents_pos)):
            self.draw_case(agents_pos[i][0], agents_pos[i][1], agents_colors[i])        
        # draw the goal
        self.draw_case(self.goal_pos[0], self.goal_pos[1], self.goal_color)
        # draw the walls
        self.draw_walls()
        cv2.imshow('board', self.board)
        # get key press
        key = cv2.waitKey(1)
        if key == ord('q'):
            return True
        return False
        
    def get_potential_moves(self, curr_pos):
        # curr_pos is a tuple of (x, y)
        # returns a list of tuples of (x, y)
        # where x and y are the potential moves
        # that the piece can make
        potential_moves = []
        # to the left
        if curr_pos[0] > 0:
            potential_moves.append((curr_pos[0] - 1, curr_pos[1]))
        # to the right
        if curr_pos[0] < self.cols - 1:
            potential_moves.append((curr_pos[0] + 1, curr_pos[1]))
        # down
        if curr_pos[1] < self.rows - 1:
            potential_moves.append((curr_pos[0], curr_pos[1] + 1))
        # up
        if curr_pos[1] > 0:
            potential_moves.append((curr_pos[0], curr_pos[1] - 1))
        # diagonal moves
        if curr_pos[0] > 0 and curr_pos[1] > 0:
            potential_moves.append((curr_pos[0] - 1, curr_pos[1] - 1))
        if curr_pos[0] < self.cols - 1 and curr_pos[1] > 0:
            potential_moves.append((curr_pos[0] + 1, curr_pos[1] - 1))
        if curr_pos[0] > 0 and curr_pos[1] < self.rows - 1:
            potential_moves.append((curr_pos[0] - 1, curr_pos[1] + 1))
        if curr_pos[0] < self.cols - 1 and curr_pos[1] < self.rows - 1:
            potential_moves.append((curr_pos[0] + 1, curr_pos[1] + 1))
        # remove walls
        for wall in self.walls:
            if wall in potential_moves:
                potential_moves.remove(wall)
        return potential_moves

        