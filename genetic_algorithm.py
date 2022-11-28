import cv2
import numpy as np
from maze_game import MazeGame, Agent

if __name__ == '__main__':
    game = MazeGame()
    agent = Agent(0, 0, agent_color=[255, 0, 0])
    # create map showing how many times each cell was visited
    visit_map = np.zeros((game.rows, game.cols), np.uint8)
    # create 8 agents
    quit = False
    while not quit:
        # display the board
        quit = game.display(agents_pos=[(agent.x, agent.y)], agents_colors=[agent.agent_color])
        # move the agent randomly
        potential_moves = game.get_potential_moves([agent.x, agent.y])
        # choose the move that has been visited the least
        min_visit = 100000
        min_visit_move = None
        for move in potential_moves:
            if visit_map[move[1], move[0]] < min_visit:
                min_visit = visit_map[move[1], move[0]]
                min_visit_move = move
        # move the agent
        agent.move(min_visit_move[0], min_visit_move[1])
        # game.agent_pos = potential_moves[np.random.randint(0, len(potential_moves))]
        # update the visit map
        visit_map[agent.y, agent.x] += 1
        # check if the agent reached the goal
        if agent.reached_goal(game.goal_pos):
            print('Agent reached the goal!')
            print('Total moves:', agent.moves)
            q = cv2.waitKey(0)
            if q == ord('q'):
                quit = True
            