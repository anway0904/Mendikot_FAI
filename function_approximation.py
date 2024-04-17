import numpy as np
import env

class LinearFunctionApproximator:
    def __init__(self, state_dim, action_dim, learning_rate=0.01):
        
        self.weights = np.zeros((action_dim, state_dim))
        self.learning_rate = learning_rate
    
    def predict(self, state):
        
        return np.dot(self.weights, state)
    
    def update(self, state, action, target):
        self.weights[action] += self.learning_rate * (target - self.predict(state)[action]) * state

def train_agent(env, function_approximator, num_episodes, discount_factor=0.9, epsilon=0.1):
    for episode in range(num_episodes):
        state = env.reset()
        done = False
        while not done:
            # Epsilon-greedy policy
            if np.random.rand() < epsilon:
                action = np.random.choice(env.action_space)
            else:
                action = np.argmax(function_approximator.predict(state))
            
            next_state, reward, done, _ = env.step(action)
            
            # Compute TD target
            td_target = reward + discount_factor * np.max(function_approximator.predict(next_state))
            
            # Update function approximator
            function_approximator.update(state, action, td_target)
            
            state = next_state

# Example usage
if __name__ == "__main__":
    # Assuming you have defined your environment and its properties
    m = env.Mendikot(cards_per_player=4)
    
    # Define state and action dimensions based on your environment
    state_dim = env.state_dim
    action_dim = env.action_dim
    
    # Initialize function approximator
    function_approximator = LinearFunctionApproximator(state_dim, action_dim)
    
    # Train the agent
    train_agent(m, function_approximator, num_episodes=1000)