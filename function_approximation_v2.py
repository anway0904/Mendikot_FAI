import numpy as np
from env import Mendikot
from MACROS import *
from tqdm import *
import matplotlib.pyplot as plt

class FunctionApproximator:
    def __init__(self, m: Mendikot, state_dim, action_dim, discount_factor=0.99, epsilon=0.01, learning_rate = 0.01):
        self.weights = np.zeros((action_dim, state_dim))
        self.m = m
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.discount_factor = discount_factor
        self.init_agent_cards = None
    
    def predict(self, state):
        vect = np.dot(self.weights, state.flatten())
        return vect
    
    def update(self, state, action, target):
        # print(action)
        action_index = np.where(action == self.init_agent_cards)[0][0]
        # print(action_index)
        self.weights[action_index,:] += self.learning_rate * (target - self.predict(state)[action_index]) * state.flatten()

    def epsilon_greedy_policy(self, state):
        '''
        Returns action according to the epsilon_greedy policy
        '''
        if np.random.rand() < self.epsilon:
            action = np.random.choice(self.m.get_available_cards(AGENT))
            return action
        else:
            available_cards = self.m.get_available_cards(AGENT)
            mask = np.isin(self.init_agent_cards ,available_cards) 
            pred_array = self.predict(state)
            action = int(np.argmin(pred_array[mask]))
            return self.init_agent_cards[action]

    def step_agent(self, state):
        action = self.epsilon_greedy_policy(state=state)
        agent_action = action
        next_state, reward, done, winner_info = self.m.step(action=action,player_type=AGENT)
        if reward != None:
            agent_reward = reward
            next_player = int(winner_info[0])
            if done:
                return next_state, agent_reward, done, agent_action
        else:
            next_player = OPPONENT_1

        
        while next_player!=AGENT:
            # print(f"PRINT DATA{self.m.get_available_cards(next_player)}")
            # print(f"PRINT DATA  {next_player}")
            action = np.random.choice(self.m.get_available_cards(next_player))
            next_state, reward, done, winner_info = self.m.step(action,next_player)
            # print(f"DONE {done}")
            if done:
                agent_reward = reward
                break

            if reward!=None:
                agent_reward = reward
                next_player = int(winner_info[0])

            else:
                next_player += 1

            if next_player == 4:
                break
        # print("END")
        return next_state, agent_reward, done, agent_action

    def train_agent(self, num_episodes):

        players = [AGENT, OPPONENT_1, TEAMMATE, OPPONENT_2]
        episode_rewards = 0
        rewards = []
        
        for episode in trange(num_episodes):
            
            # Starting new game 
            # Select random player to start new game
            # TO-DO : Can change this to winner of previous game in future versions

            next_player = np.random.choice(len(players))
            state = m.reset()
            done = False
            

            self.init_agent_cards = self.m.get_cards_in_hand(AGENT)
            
            while not done:

                next_state, reward, done, agent_action = self.step_agent(state)
                # print(reward)
                td_target = reward + self.discount_factor * np.max(self.predict(next_state))
                
                self.update(state=state,action=agent_action,target=td_target)

                state = next_state
                episode_rewards += reward

            rewards.append(episode_rewards)
            # print(f"Episode {episode} Rewards : {episode_rewards}")
            episode_rewards = 0

        return rewards, self.weights


if __name__ == "__main__":
    
    m = Mendikot(cards_per_player=4)
    _ = m.reset()
    
    state_dim = m.get_state().flatten().shape[0]
    action_dim = m.cards_per_player
    # print(action_dim)
    
    # Initialize function approximator
    function_approximator = FunctionApproximator(m, state_dim, action_dim,discount_factor=0.99, epsilon=0.1,learning_rate=0.1)
    
    # # Train the agent
    rewards, weights = function_approximator.train_agent(num_episodes=100000)

    # print(weights[0].reshape(9,16))
    plt.plot(rewards)
    plt.show()