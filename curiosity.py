import cv2
import numpy as np
from maze_game import MazeGame

if __name__ == '__main__':
    game = MazeGame()
    # create map showing how many times each cell was visited
    visit_map = np.zeros((game.rows, game.cols), np.uint8)
    quit = False
    while not quit:
        # display the board
        quit = game.display()
        # move the agent randomly
        potential_moves = game.get_potential_moves(game.agent_pos)
        # choose the move that has been visited the least
        min_visit = 100000
        min_visit_move = None
        for move in potential_moves:
            if visit_map[move[1], move[0]] < min_visit:
                min_visit = visit_map[move[1], move[0]]
                min_visit_move = move
        game.move_agent(min_visit_move[0], min_visit_move[1])
        # game.agent_pos = potential_moves[np.random.randint(0, len(potential_moves))]
        # update the visit map
        visit_map[game.agent_pos[1], game.agent_pos[0]] += 1
        # check if the agent reached the goal
        if game.agent_reached_goal():
            print('Agent reached the goal!')
            print('Total moves:', game.total_moves)
            q = cv2.waitKey(0)
            if q == ord('q'):
                quit = True
            