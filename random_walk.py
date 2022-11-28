import cv2
import numpy as np
from maze_game import MazeGame, Agent

if __name__ == '__main__':
    game = MazeGame()
    agent = Agent(0, 0, agent_color=[255, 0, 0])
    quit = False
    while not quit:
        # display the board
        quit = game.display(agents_pos=[(agent.x, agent.y)], agents_colors=[agent.agent_color])
        # move the agent randomly
        potential_moves = game.get_potential_moves([agent.x, agent.y])
        potential_move = potential_moves[np.random.randint(0, len(potential_moves))]
        agent.move(potential_move[0], potential_move[1])
        # check if the agent reached the goal
        if agent.reached_goal(game.goal_pos):
            print('Agent reached the goal!')
            print('Total moves:', agent.moves)
            q = cv2.waitKey(0)
            if q == ord('q'):
                quit = True