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

CARD_FOR_PLAYING        = 0
CARD_IN_HAND_AGENT      = 1
CARD_IN_HAND_OPPNT_1    = 2
CARD_IN_HAND_TEAM       = 3
CARD_IN_HAND_OPPNT_2    = 4
CARD_AVAILABLE          = 5
CARD_CURR_TRICK_AGENT   = 6
CARD_CURR_TRICK_OPPNT_1 = 7
CARD_CURR_TRICK_TEAM    = 8
CARD_CURR_TRICK_OPPNT_2 = 9
CARD_PREV_TRICK_AGENT   = 10
CARD_PREV_TRICK_OPPNT_1 = 11
CARD_PREV_TRICK_TEAM    = 12
CARD_PREV_TRICK_OPPNT_2 = 13
CARD_TRUMP              = 14

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

class Mendikot():
    def __init__(self, cards_per_player: int = 4) -> None:
        self.cards_deck = 52
        self.game_features = 15
        self.game_matrix = np.zeros([self.cards_deck, self.game_features])

        assert (cards_per_player >= 4) and (cards_per_player <=13), "Invalid cards per player. Valid range of cards per player is [4, 13]"
        self.cards_per_player = cards_per_player
        
        self.min_cards = [CARDS.index('T'), CARDS.index('A'), CARDS.index('K'), CARDS.index('Q')]
        
    def reset(self) -> tuple[np.ndarray, str]:
        """
        Resets and starts over the game. Distributes the cards specified by self.cards_per_player. 
        Minimum 4 cards per player (10, A, K, Q) followed by J, 10, 9, 8 ... 2
        """
        self.game_matrix *= 0
        self.game_matrix[CARD_IDX[self.min_cards,:].flatten(), CARD_FOR_PLAYING] = 1
        
        trump_suit = np.random.choice(SUITS)
        self.game_matrix[CARD_IDX[:,SUITS.index(trump_suit)], CARD_TRUMP] = 1

        if self.cards_per_player > len(self.min_cards):
            self.game_matrix[CARD_IDX[CARDS.index('J'),:], CARD_FOR_PLAYING] = 1
            idx_e = len(CARDS) - (len(self.min_cards) + 1)
            idx_s = idx_e - (self.cards_per_player - (len(self.min_cards) + 1))
            self.game_matrix[CARD_IDX[idx_s:idx_e, :].flatten(), CARD_FOR_PLAYING] = 1 

        total_cards_in_play = self.get_cards_in_play()
        np.random.shuffle(total_cards_in_play)
        
        self.game_matrix[total_cards_in_play[0:self.cards_per_player], CARD_IN_HAND_AGENT]    = 1
        self.game_matrix[total_cards_in_play[1*self.cards_per_player : 2*self.cards_per_player], CARD_IN_HAND_OPPNT_1]  = 1
        self.game_matrix[total_cards_in_play[2*self.cards_per_player : 3*self.cards_per_player], CARD_IN_HAND_TEAM]     = 1
        self.game_matrix[total_cards_in_play[3*self.cards_per_player : 4*self.cards_per_player], CARD_IN_HAND_OPPNT_2]  = 1

        # raise NotImplementedError("Need to return state!!!!!!!!!!! Discuss what state should be")

    def get_cards_in_play(self) -> tuple[int]:
        idx = np.where(self.game_matrix[:,CARD_FOR_PLAYING] == 1)[0]
        return idx
    
    def get_cards_in_trick(self) -> tuple[int]:
        idx = np.where(self.game_matrix[:,CARD_CURR_TRICK_AGENT:CARD_CURR_TRICK_OPPNT_2+1] == 1)[0]
        return idx
    
    def get_cards_in_hand(self, player : int) -> tuple[int]:
        if player == AGENT:
            idx = np.where(self.game_matrix[:,CARD_IN_HAND_AGENT] == 1)[0]
        if player == OPPONENT_1:
            idx = np.where(self.game_matrix[:,CARD_IN_HAND_OPPNT_1] == 1)[0]
        if player == OPPONENT_2:
            idx = np.where(self.game_matrix[:,CARD_IN_HAND_OPPNT_2] == 1)[0]
        if player == TEAMMATE:
            idx = np.where(self.game_matrix[:,CARD_IN_HAND_TEAM] == 1)[0]

        return idx
    
    def step(self, action: int, player_type: int):
        '''
        action is a card from hand the agent should play
        every card has a unique integer from 0 to 51
        1. Access the game matrix
        2. Update required for following cards in the matrix:
            a. card choosen 
            b. previously choosen card -> update its status - not sure
        '''
        
        if action in self.get_cards_in_hand(player=player_type):
            self.game_matrix[action, CARD_AVAILABLE] = 0
            
            if player_type == AGENT:
                self.game_matrix[action, CARD_CURR_TRICK_AGENT] = 1
                self.game_matrix[action, CARD_IN_HAND_AGENT] = 0
                
            if player_type == OPPONENT_1:
                self.game_matrix[action, CARD_CURR_TRICK_OPPNT_1] = 1
                self.game_matrix[action, CARD_IN_HAND_OPPNT_1] = 0

            if player_type == OPPONENT_2:
                self.game_matrix[action, CARD_CURR_TRICK_OPPNT_2] = 1
                self.game_matrix[action, CARD_IN_HAND_OPPNT_2] = 0

            if player_type == TEAMMATE:
                self.game_matrix[action, CARD_CURR_TRICK_TEAM] = 1
                self.game_matrix[action, CARD_IN_HAND_TEAM] = 0
        else:
            print(f"INVALID_ACTION : card not in hand for {player_type}")
        

    def update_game(self):
        
        current_cards = self.get_cards_in_trick()
        if  len(current_cards) == 4:
            '''
            TRICK OVER 
            Update the score matrix
            '''
            # self.game_matrix[current_cards,CARD_PREV_TRICK_AGENT] = 1
            # self.game_matrix[current_cards,CARD_CURR_TRICK_AGENT] = 0
            print(self.game_matrix[current_cards,:])
        
            cols = np.where(self.game_matrix[:,CARD_CURR_TRICK_AGENT:CARD_CURR_TRICK_OPPNT_2+1] == 1)[1]
            cols += 10
            self.game_matrix[current_cards,cols] = 1
            self.game_matrix[current_cards,:]
            self.game_matrix[:,CARD_CURR_TRICK_AGENT:CARD_CURR_TRICK_OPPNT_2+1] = 0
            print(self.game_matrix[current_cards,:])

            # print(np.where(self.game_matrix[current_cards,CARD_CURR_TRICK_AGENT:CARD_CURR_TRICK_OPPNT_2] == 1) == 1[0])
            # self.game_matrix[current_cards,]

            # for card in current_cards:
            #     if self.game_matrix[card,CARD_CURR_TRICK_AGENT] == 1:
            #         self.game_matrix[card,CARD_PREV_TRICK_AGENT] = 1
            #         self.game_matrix[card,CARD_CURR_TRICK_AGENT] = 0

            #     elif self.game_matrix[card,CARD_CURR_TRICK_OPPNT_1] == 1:
            #         self.game_matrix[card,CARD_PREV_TRICK_OPPNT_1] = 1
            #         self.game_matrix[card,CARD_CURR_TRICK_OPPNT_1] = 0

            #     elif self.game_matrix[card,CARD_CURR_TRICK_OPPNT_2] == 1:
            #         self.game_matrix[card,CARD_PREV_TRICK_OPPNT_2] = 1
            #         self.game_matrix[card,CARD_CURR_TRICK_OPPNT_2] = 0

            #     else:
            #         self.game_matrix[card,CARD_PREV_TRICK_TEAM] = 1
            #         self.game_matrix[card,CARD_CURR_TRICK_TEAM] = 0                    

        



        