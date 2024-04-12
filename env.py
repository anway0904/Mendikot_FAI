'''
Environment V0.0

Project : Mendikot
Authors : Neeraj, Anway
Date : 4-11-24


Game represented by a matrix where each row corresponds to a card and each column represents a feature
The features are:

Card considered for playing (Used to determine number of cards used for playing the game [min 4])
Card in your hand
Card available/legal to be played
Card in current trick played by agent
Card in current trick played by opponent
Card in current trick played by teammate
Card in previous trick played by agent
Card in previous trick played by opponent
Card in previous trick played by teammate
Card in trump suite

CARD_FOR_PLAYING = 0
CARD_IN_HAND = 1
CARD_AVAILABLE = 2
CARD_CURR_TRICK_AGENT = 3
CARD_CURR_TRICK_OPPNT_1 = 4
CARD_CURR_TRICK_TEAM = 5
CARD_CURR_TRICK_OPPNT_2 = 6
CARD_PREV_TRICK_AGENT = 7
CARD_PREV_TRICK_OPPNT_1 = 8
CARD_PREV_TRICK_TEAM = 9
CARD_PREV_TRICK_OPPNT_1 = 10
CARD_TRUMP = 11

52x10 matrix represents the entire game

Score Matrix:
Each row belongs to a player (including the agent)

		Tricks won	Tricks won with 10	Teammate/Opponent (1 for teammate, 0 for opponent)
Agent		1		1			1			
Player 2	2		2			0
Player 3	0		0			1
Player 4	1		1			0


Rewards:
+5: Trick won with a 10 (By you or teammate)
+1: Trick won without a 10 (By you or teammate)
-5: Trick won with a 10 (By opponents)
-1: Trick won without a 10 (By opponent)
'''
import numpy as np
import random
from MACROS import *
import MACROS
class Mendikot():
    def __init__(self) -> None:
        self.cards_deck = 52
        self.game_features = 12
        self.game_matrix = np.zeros([self.cards_deck, self.game_features])
        self.cards_per_player = 4
        self.suits = ['S', 'H', 'C', 'D']
        
    def reset(self) -> tuple[np.ndarray, str]:
        """
        Resets and starts over the game. Distributes the cards specified by self.cards_per_player. 
        Minimum 4 cards per player (10, A, K, Q) followed by J, 10, 9, 8 ... 2
        """
        
        
    
    def step(self, action: int, player_type: int):
        '''
        action is a card from hand the agent should play
        every card has a unique integer from 0 to 51
        1. Access the game matrix
        2. Update required for following cards in the matrix:
            a. card choosen 
            b. previously choosen card -> update its status - not sure
        '''
        self.game_matrix[action, CARD_IN_HAND] = 0
        self.game_matrix[action, CARD_AVAILABLE] = 0
        self.game_matrix[action, CARD_CURR_TRICK_AGENT] = 1

        if player_type == AGENT:
            self.game_matrix[action, CARD_CURR_TRICK_AGENT] = 1
        elif player_type == OPPONENT_1:
            self.game_matrix[action, CARD_CURR_TRICK_OPPNT_1] = 1
        elif player_type == OPPONENT_2:
            self.game_matrix[action, CARD_CURR_TRICK_OPPNT_2] = 1
        else:
            self.game_matrix[action, CARD_CURR_TRICK_TEAM] = 1
        

    def update_game(self):
        card_count = np.sum(self.game_matrix[:,CARD_CURR_TRICK_AGENT:CARD_CURR_TRICK_OPPNT_2])
            
    