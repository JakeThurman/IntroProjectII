#Card War Project - Jacob Thurman and Thomas Frick
import pygame, sys, random

# VARIABLE DECLERATION

# control variable for the loop
warMongering = True
# the first player's stack of 26 cards
player_1_deck = []
# the second player's stack of 26 cards
player_2_deck = []
# the first player's play area
player_1_battlefield = []
# the second player's play area
player_2_battlefield = []
# the first player's score
player_1_score = 0
# the second player's score
player_2_score = 0
# the deck of cards the game is played with.
#  Used cards will be discarded into the deck
#  The string at index 0 of each item is the name of that card's image
#  The number at index 1 of each item is that card's value
deck = [["SA", 14], ["S2", 2], ["S3", 3], ["S4", 4], ["S5", 5], ["S6", 6],
        ["S7", 7], ["S8", 8], ["S9", 9], ["S0", 10], ["SJ", 11], ["SQ", 12],
        ["SK", 13],
        ["HA", 14], ["H2", 2], ["H3", 3], ["H4", 4], ["H5", 5], ["H6", 6],
        ["H7", 7], ["H8", 8], ["H9", 9], ["H0", 10], ["HJ", 11], ["HQ", 12],
        ["HK", 13],
        ["CA", 14], ["C2", 2], ["C3", 3], ["C4", 4], ["C5", 5], ["C6", 6],
        ["C7", 7], ["C8", 8], ["C9", 9], ["C0", 10], ["CJ", 11], ["CQ", 12],
        ["CK", 13],
        ["DA", 14], ["D2", 2], ["D3", 3], ["D4", 4], ["D5", 5], ["D6", 6],
        ["D7", 7], ["D8", 8], ["D9", 9], ["D0", 10], ["DJ", 11], ["DQ", 12],
        ["DK", 13]]

#FUNCTIONS

# shuffles the contents of deck
def shuffle():
    random.shuffle(deck)
    
# distributes the contents of deck evenly into both decks
def gather_army():
	""" split_list """

    player_1 = True
    while len(deck) != 0:
        if player_1 == True:
            player_1_deck.append(deck[0])
            deck.remove(deck[0])
            player_1 = ~player_1
        else:
            player_2_deck.append(deck[0])
            deck.remove(deck[0])
            player_1 = ~player_1

# plays the next card in each players deck into each player's battlefield
def ready_forces():
    # TO DO: WRITE A CHECK TO SEE IF WE STILL HAVE CARDS
    # returns False if player decks are empty

    # display player 1's next card
    print(player_1_deck[0][0])
    player_1_battlefield.append(player_1_deck[0])
    player_1_deck.remove(player_1_deck[0])

    # display player 2's next card
    print(player_2_deck[0][0], "\n")
    player_2_battlefield.append(player_2_deck[0])
    player_2_deck.remove(player_2_deck[0])

    # stop the game if we run out of cards
    if (len(player_1_deck) == 0 or len(player_2_deck) == 0):
        return False
        
    return True
    

# compare the cards on the battlefield. 
def skirmish():
    global player_1_score, player_2_score
    player_1_card = player_1_battlefield[len(player_1_battlefield)-1]
    player_2_card = player_2_battlefield[len(player_2_battlefield)-1]
    # Player 1 wins the skirmish
    if(player_1_card[1] > player_2_card[1]):
        print("Player 1 has won this skirmish!")
        player_1_score = player_1_score + player_1_card[1]
    # Player 2 wins the skirmish
    if(player_1_card[1] < player_2_card[1]):
        print("Player 2 has won this skirmish!")
        player_2_score = player_2_score + player_2_card[1]
    # The Players have tied
    if (player_1_card[1] == player_2_card[1]):
        print("The battlefield is evenly matched!\nSearch your army for a champion!\n")
        find_the_champion()

# used in the event of a tie in a skirmish. Draws the next 3 cards
# in each player's deck and has the third card skirmish
def find_the_champion():
    global warMongering, player_1_score, player_2_score

    # draw three cards. If you can't draw another card,
    #   calls the endgame function
    if warMongering:
       warMongering = ready_forces()
    else:
        print("The armies are out of resources. Time to return home...")
        abandon_the_battlefield()
    if warMongering:
        warMongering = ready_forces()
    else:
        print("The armies are out of resources. Time to return home...")
        abandon_the_battlefield()
    if warMongering:
        warMongering = ready_forces()
    else:
        print("The armies are out of resources. Time to return home...")
        abandon_the_battlefield()
    player_1_card = player_1_battlefield[len(player_1_battlefield)-1]
    player_2_card = player_2_battlefield[len(player_2_battlefield)-1]
    # Player 1 wins the skirmish
    if(player_1_card[1] > player_2_card[1]):
        print("\nPlayer 1 has won this skirmish!")
        player_1_score += player_1_card[1]
    # Player 2 wins the skirmish
    if(player_1_card[1] < player_2_card[1]):
        print("\nPlayer 2 has won this skirmish!")
        player_2_score += player_2_card[1]
    # The Players have tied
    if (player_1_card[1] == player_2_card[1]):
        print("\nThe battle has ended in a stalemate")

# Display the player scores and end the game
def abandon_the_battlefield():
    if player_1_score > player_2_score:
        print("Player 1 has conquered the battlefield!")
    if player_1_score < player_2_score:
        print("Player 2 has conquered the battlefield!")
    if player_1_score == player_2_score:
        print("Night falls on an empty battlefield stained in blood.",
              "\nThere are no winners in war...")

# Loops through a card war
def the_war_never_ends():
    global warMongering
    warMongering = True
    shuffle()
    gather_army()
    while(warMongering):
        warMongering = ready_forces()
        skirmish()
        print("\nPlayer 1 Score:", player_1_score)
        print("Player 2 Score:", player_2_score)
        if warMongering:
            print("\nPress enter to continue")
            input()

    abandon_the_battlefield()
    return True;

# moves the cards in each player's battlefield to the deck
def recover_from_the_war():
    global player_1_score, player_2_score
    while(len(player_1_battlefield)!=0):
        deck.append(player_1_battlefield[0])
        player_1_battlefield.remove(player_1_battlefield[0])
    while(len(player_2_battlefield)!=0):
        deck.append(player_2_battlefield[0])
        player_2_battlefield.remove(player_2_battlefield[0])
    player_1_score = 0
    player_2_score = 0
    

# MAIN LOOP

# Exposition and stuff
print("Your kingdom is in desperate need of resources")
print("Your citizens are starving, your buildings are falling apart, and your crops are failing")
print("There is only one hope:")
input()
print("CARDTOPIA")
input()
print("Bountiful in wealth and resouces, this beautiful land",
      "\nholds everything you need to restore your country.",
      "\nBut there is a rival. They also wish to take Cardtopia",
      "\nfor themselves, and they aren't interested in sharing.",
      "\nSo gather your armies! Fight for your country! It's time...",
      "\nfor a CARD WAR!\n")
# The actual loop
while True:
    the_war_never_ends()
    print("The battle is over for now...but there will always be those who covet Cardtopia\'s resources")
    inp = input("Defend Cardtopia again? Y/N")
    if inp.upper() != "Y":
        break;
    recover_from_the_war()
print("Thank you for playing Card Wars!")
