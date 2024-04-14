'''
Environment V0.0

Project : Mendikot
Authors : Neeraj Sahasrabudhe, Anway Shirgaonkar
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

		Tricks won	Tricks won with 10
AGENT		1		1						
OPPNT_1		2		2	
TEAM     	0		0			
OPPNT_2 	1		1			

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
        self.num_players = 4
        self.cards_deck = 52
        self.game_features = 15
        self.score_features = 2
        self.game_matrix = np.zeros([self.cards_deck, self.game_features])
        self.score_matrix = np.zeros([self.num_players, self.score_features])
        self.curr_trick = np.array([], dtype=int)

        assert (cards_per_player >= 4) and (cards_per_player <=13), "Invalid cards per player. Valid range of cards per player is [4, 13]"
        self.cards_per_player = cards_per_player
        
        self.min_cards = [CARDS.index('T'), CARDS.index('A'), CARDS.index('K'), CARDS.index('Q')]
        self.trump_suit = None
        self.trick_suit = None

    def reset(self) -> tuple[np.ndarray, str]:
        """
        Resets and starts over the game. Distributes the cards specified by self.cards_per_player. 
        Minimum 4 cards per player (10, A, K, Q) followed by J, 10, 9, 8 ... 2
        """
        # Reset the game matrix
        self.game_matrix *= 0

        # Set CARD_FOR_PLAYING the min cards required to play 
        self.game_matrix[CARD_IDX[self.min_cards,:].flatten(), CARD_FOR_PLAYING] = 1
        
        # Set CARD_FOR_PLAYING for additional cards as per cards per player flag
        if self.cards_per_player > len(self.min_cards):
            self.game_matrix[CARD_IDX[CARDS.index('J'),:], CARD_FOR_PLAYING] = 1
            idx_e = len(CARDS) - (len(self.min_cards) + 1)
            idx_s = idx_e - (self.cards_per_player - (len(self.min_cards) + 1))
            self.game_matrix[CARD_IDX[idx_s:idx_e, :].flatten(), CARD_FOR_PLAYING] = 1 

        # Get the total cards in play and shuffle randomly
        total_cards_in_play = self.get_cards_in_play()

        np.random.shuffle(total_cards_in_play)
        np.random.shuffle(total_cards_in_play)
        np.random.shuffle(total_cards_in_play)

        # Distribute the cards among players by setting the CARD_IN_HAND flag
        self.game_matrix[total_cards_in_play[0:self.cards_per_player], CARD_IN_HAND_AGENT]    = 1
        self.game_matrix[total_cards_in_play[1*self.cards_per_player : 2*self.cards_per_player], CARD_IN_HAND_OPPNT_1]  = 1
        self.game_matrix[total_cards_in_play[2*self.cards_per_player : 3*self.cards_per_player], CARD_IN_HAND_TEAM]     = 1
        self.game_matrix[total_cards_in_play[3*self.cards_per_player : 4*self.cards_per_player], CARD_IN_HAND_OPPNT_2]  = 1

        # Randomly select the trump suit and set the CARD_TRUMP flag
        self.trump_suit = np.random.choice(SUITS)
        self.game_matrix[CARD_IDX[:,SUITS.index(self.trump_suit)], CARD_TRUMP] = 1

        # raise NotImplementedError("Need to return state!!!!!!!!!!! Discuss what state should be")

    def get_render_str(self, card_idx: int = None, card:str = None, suit:str = None, cards_list:list = None):
        if card_idx != None:
            card, suit = self.get_card(card_idx)
            string = f"{card}{SUITS_RENDER[suit]}"

        elif card != None and suit != None:
            string = f"{card}{SUITS_RENDER[suit]}"

        elif cards_list.all() != None:
            string = ""
            for card in cards_list:
                card, suit = self.get_card(card)
                string += f"{card}{SUITS_RENDER[suit]} "

        # print(string)
        return string

    
    def get_card(self, card : int):
        num_idx, suit_idx = np.where(CARD_IDX[:,:] == card)
        num = CARDS[num_idx[0]]
        suit = SUITS[suit_idx[0]]
        return num, suit
        # return num_idx[0], suit_idx[0]

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
    
    def get_cards_in_prev_trick(self, player : int) -> tuple[int]:
        if player == AGENT:
            idx = np.where(self.game_matrix[:,CARD_PREV_TRICK_AGENT] == 1)[0]
        if player == OPPONENT_1:
            idx = np.where(self.game_matrix[:,CARD_PREV_TRICK_OPPNT_1] == 1)[0]
        if player == OPPONENT_2:
            idx = np.where(self.game_matrix[:,CARD_PREV_TRICK_OPPNT_2] == 1)[0]
        if player == TEAMMATE:
            idx = np.where(self.game_matrix[:,CARD_PREV_TRICK_TEAM] == 1)[0]
        return idx
    
    def get_trump_in_trick(self):
        return np.where(self.game_matrix[self.curr_trick, CARD_TRUMP] == 1)[0]

    def get_winner(self, cards : list[int]) -> int:
        assert (len(cards)==4) and (len(self.curr_trick)==4), "get_winner invoked when trick size != 4"
        # print(f"Trump: {SUITS_RENDER[self.trump_suit]}")

        idx_trumps_in_trick = self.get_trump_in_trick()
        if len(idx_trumps_in_trick) != 0:
            winner_card_idx = max(self.curr_trick[idx_trumps_in_trick])
            winner_card, _ = self.get_card(winner_card_idx)
            print(f"WINNER! {winner_card}{SUITS_RENDER[self.trump_suit]}")

        else:    
            winner_card_idx = -1
            for card in self.curr_trick:
                _, card_suit = self.get_card(card)
                if (card_suit == self.trick_suit) and (card > winner_card_idx):
                    winner_card_idx = card

            winner_card, _ = self.get_card(winner_card_idx)
            print(f"WINNER! {winner_card}{SUITS_RENDER[self.trick_suit]}")    
        
        print(self.get_card(winner_card_idx))
        return (np.where(self.game_matrix[winner_card_idx,CARD_CURR_TRICK_AGENT:CARD_CURR_TRICK_OPPNT_2+1])[0][0])
    
    def get_available_cards(self, player_type: int):
        self.game_matrix[:, CARD_AVAILABLE] = 0
        cards_in_hand = self.get_cards_in_hand(player_type)

        if self.trick_suit == None:
            self.game_matrix[cards_in_hand, CARD_AVAILABLE] = 1

        for card in cards_in_hand:
            _, suit = self.get_card(card)
            if suit == self.trick_suit:
                self.game_matrix[card,CARD_AVAILABLE] = 1

        if not np.any(self.game_matrix[cards_in_hand,CARD_AVAILABLE]):
            self.game_matrix[cards_in_hand,CARD_AVAILABLE] = 1

        return np.where(self.game_matrix[:,CARD_AVAILABLE] == 1)[0]

    def is_trick_empty(self):
        return True if len(self.curr_trick) == 0 else False
    
    def step(self, action: int, player_type: int):
        '''
        action is a card from hand the agent should play
        every card has a unique integer from 0 to 51
        1. Access the game matrix
        2. Update required for following cards in the matrix:
            a. card choosen 
            b. previously choosen card -> update its status - not sure
        '''
        assert np.any(self.game_matrix[:, CARD_AVAILABLE]), "Please call get_available_cards() first"
        if self.is_trick_empty():
            _, self.trick_suit = self.get_card(action)

        self.curr_trick = np.append(self.curr_trick, action)        
        
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

        self.game_matrix[:, CARD_AVAILABLE] = 0
    
    def evaluate_trick(self):
        current_cards = self.get_cards_in_trick()
        if  len(current_cards) == 4:
            '''
            TRICK OVER 
            Update the score matrix
            '''
            # Update Game Matrix
            winner_player = self.get_winner(current_cards)
            

            # Update Previous Trick Parameters
            cols = np.where(self.game_matrix[:,CARD_CURR_TRICK_AGENT:CARD_CURR_TRICK_OPPNT_2+1] == 1)[1] # Returns Columns for cards from CARD_CURR_TRICK_AGENT:CARD_CURR_TRICK_OPPNT_2
            cols += CARD_PREV_TRICK_AGENT
            self.game_matrix[current_cards,cols] = 1
            
            # Update Current Trick Parameters
            self.game_matrix[:,CARD_CURR_TRICK_AGENT:CARD_CURR_TRICK_OPPNT_2+1] = 0

            return winner_player
