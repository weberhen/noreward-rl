import cv2
import numpy as np
from maze_game import MazeGame

if __name__ == '__main__':
    game = MazeGame()
    quit = False
    while not quit:
        # display the board
        quit = game.display()
        # move the agent randomly
        potential_moves = game.get_potential_moves(game.agent_pos)
        potential_move = potential_moves[np.random.randint(0, len(potential_moves))]
        game.move_agent(potential_move[0], potential_move[1])
        # check if the agent reached the goal
        if game.agent_reached_goal():
            print('Agent reached the goal!')
            print('Total moves:', game.total_moves)
            q = cv2.waitKey(0)
            if q == ord('q'):
                quit = True