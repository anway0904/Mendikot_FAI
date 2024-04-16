import numpy as np
import env
from MACROS import *
from tqdm import trange

num_trials = 10000

m = env.Mendikot(cards_per_player = 5)

_ = m.reset()
terminated = False
next_player = int(np.random.choice(3))

agent_wins = 0

for _ in trange(num_trials):
    while not terminated:
        for iter in range(4):
            player = (next_player+iter) % 4

            # All players employ random policy
            choice = np.random.choice(m.get_available_cards(player))

            # Play 1 card - 1 step in the environment
            next_state, reward, terminated, winner_info = m.step(choice,player)

        next_player = int(winner_info[0])

    if m.get_game_winner() == AGENT:
        agent_wins = agent_wins + 1

    _ = m.reset()
    terminated = False
    next_player = int(np.random.choice(3))

print(f"Percentage Win: {agent_wins/num_trials*100.0} %")