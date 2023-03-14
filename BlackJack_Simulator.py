# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 19:43:19 2022

Below is a simulation of a simplified version of the game of Blackjack. Only two participants are active for each game,
one player and the dealer, cards are drawn for the "other players" but they do not take part. This version of Blackjack
does not include the ability to Double or Split, players can only Hit or Hold. Player decision making is decided before
each game begins and follows a set of rules that don't change.

"""

import random

#### CREATE FUNCTIONS ####
# Function to prepare and shuffle 4 decks of cards
def new_deck():
    newdeck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]*16
    random.shuffle(newdeck)
    
    return newdeck

# Function to deal cards
def deal_card(pack, hand):
    drawncard = pack.pop()
    hand.append(drawncard)


# Player function - output 0 if they want to hold or 1 if they want another card
def player(player_cards, dealer_cards, otherplayers_cards):
    player_total = sum(player_cards)
    dealer_total = sum(dealer_cards)
    otherplayers_total = sum(otherplayers_cards)
    # default decision: 0 = hold 1 = hit
    decision = 0
    if player_total < 12:
        decision = 1
    elif player_total < 16 and dealer_total >= 7 and otherplayers_total >= 65:
        decision = 1
        
    return decision

# Dealer function - output 0 if they want to hold or 1 if they want another card
def dealer(dealer_cards):
    dealer_total = sum(dealer_cards)
    # default decision: 0 = hold 1 = hit
    decision = 0
    if dealer_total < 17:
        decision = 1
    
    return decision

# Function to change value of ace from 11 to 1 if required
def check_for_aces(cards):
    cards.sort()
    if sum(cards) > 21 and cards[-1] == 11:
        cards[-1] = 1

# Function to check hands for blackjack        
def check_for_blackjack(cards):
    blackjack = 0
    if len(cards) == 2 and sum(cards) == 21:
        blackjack = 1
    
    return blackjack
    
# Main function for blackjack simulator    
def blackjack_game():
## START WITH A NEW DECK ##
    deck = new_deck()
    player_wins = 0
    dealer_wins = 0
    draws = 0
    # iterate 1000 games
    for i in range(1000):
        # If deck gets below 50 cards get a new deck before next hand
        if len(deck) < 50:
            deck = new_deck()
            
        # player, dealer and other players hands (clear before each new hand)
        player_hand = []
        dealer_hand = []
        otherplayers_hand = []
        
## DEAL THE CARDS ## 
        # each player gets 2 cards to start except the dealer who gets 1
        for n in range (2):
            for j in range(5):
                # last player is "The Player"
                if j == 3:
                    deal_card(deck,player_hand)
                # "The Dealer" has their card dealt last and only once
                elif j == 4:
                    if n == 0:
                        deal_card(deck, dealer_hand)
                else:
                    deal_card(deck, otherplayers_hand)
        
        for n in range(4): # draw 4 more cards per game for other players
            deal_card(deck, otherplayers_hand)

## PLAYER PLAYS ##
        # check for blackjack or if 2 aces in hand
        if check_for_blackjack(player_hand) == 0:
            check_for_aces(player_hand)
                    
        # player hits or holds depending on their cards and the dealer's
            hit_or_hold = player(player_hand,dealer_hand,otherplayers_hand)
            while hit_or_hold == 1:
                deal_card(deck,player_hand)
                check_for_aces(player_hand)
                 # player busts if total of hand over 21   
                if sum(player_hand) > 21:   
                    break
                else:
                    hit_or_hold = player(player_hand,dealer_hand,otherplayers_hand)
       
## DEALER PLAYS ##    
            if sum(player_hand) <= 21: # check player hasn't busted
                deal_card(deck,dealer_hand)
                if check_for_blackjack(dealer_hand) == 0:
                    check_for_aces(dealer_hand)
                    # dealer draws a card if total of their hand is less than 17
                    hit_or_hold = dealer(dealer_hand)
                    while hit_or_hold == 1:
                        deal_card(deck,dealer_hand)
                        check_for_aces(dealer_hand)
                        # dealer busts if total of hand over 21
                        if sum(dealer_hand) > 21:
                            break
                        else:
                            hit_or_hold = dealer(dealer_hand)
                
                else: # dealer blackjack
                    dealer_wins += 1
                    
        else: # player blackjack
            player_wins += 1
            
## COMPARE HANDS AND CHECK RESULTS ##    
        if check_for_blackjack(player_hand) == 0 and check_for_blackjack(dealer_hand) == 0:
            if sum(player_hand) > 21:
                dealer_wins += 1
            elif sum(dealer_hand) > 21:
                player_wins += 1
            elif sum(player_hand) > sum(dealer_hand):
                player_wins += 1
            elif sum(player_hand) < sum(dealer_hand):
                dealer_wins += 1
            else:
                draws += 1

    
## PRINT RESULTS TO SCREEN ##
    print("\033[H\033[J", end="")
    print("All Blackjack games played")
    print("Player Wins: ", player_wins)
    print("Player Win %: ", round(player_wins / (i)*100,1))
    print("Dealer Wins: ", dealer_wins)
    print("Dealer Win %: ", round(dealer_wins / (i)*100,1))
    print("Draws: ", draws)
    print("Draw %: ", round(draws / (i)*100,1))

#### MAIN PROGRAM ####

blackjack_game()