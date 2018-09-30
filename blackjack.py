'''
Blackjack game in python.
This is a basic implementation of blackjack where the dealer is the computer itself,and it keeps on hitting until it wins
or surpasses player's total(the player has the first turn).This game does not support advanced functionalities such as 
double-down,card split etc.
'''


import random   #for shuffling the decks

suits=('Hearts','Diamonds','Spades','Clubs')
ranks=('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values={'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11}

class Card: 

    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank

    def __str__(self):
        return self.rank+" of "+self.suit

class Deck: 

    def __init__(self): #for storing all the cards in the deck
        self.deck=[]
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):  #for printing out the cards in the deck
        deck_comp=''
        for card in self.deck:
            deck_comp+='\n'+card.__str__()
        return "the deck has: "+deck_comp

    def shuffle(self):  #for shuffling
        random.shuffle(self.deck)

    def deal(self): #for returning a single card if a player wants to deal
        single_card=self.deck.pop()
        return single_card

class HumanPlayer:  

    def __init__(self): #storing all the cards of human player,their value and the number of aces
        self.cards=[]
        self.value=0
        self.aces=0

    def add_card(self,card):    #adding card if human player wants a 'hit'
        self.cards.append(card)
        self.value+=values[card.rank]

        if card.rank=='Ace':
            self.aces+=1

    def adjust_for_ace(self):   #assigns value 1 to an ace if the total of human player exceeds 21 else its value is 11
        while self.value>21 and self.aces:
            self.value-=10
            self.aces-=1

class Chips:

    def __init__(self,total):   #for storing total number of chips of the player
        self.total=total
        self.bet=0

    def win_bet(self):  #adding the winning amount to a player's total chips
        self.total+=self.bet

    def lose_bet(self): #subtracting the losing amount to a player's total chips
        self.total-=self.bet

def take_bet(chips):    #for checking whether the player has the required number of chips to take a bet
    
    while True:
        try:
            chips.bet=int(input('enter the number of chips you would like to bet on:'))
        except ValueError:
            print('incorrect input,a bet must be an integer!')
        else:
            if chips.bet>chips.total:
                print(f"Sorry, your bet can't exceed {chips.total}")
            else:
                break

def hit(deck,hand): #for adding a card to the player's deck if it is a hit and checking for the total value of cards
    
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):    #for asking player whether he/she wants to take a hit or stand

    global playing  
    
    while True:
        x=input("Would you like to Hit or Stand? Enter 'h' or 's':")
        
        if x=='h' and len(x)==1:
            hit(deck,hand)  

        elif x=='s' and len(x)==1:
            print("Player stands, Dealer is playing.")
            playing=False

        else:
            print("incorrect input")
            continue
        break

def show_some(player,dealer):   #for showing dealer's card and all cards of the player
    print("\nDealer's Hand:")
    print("<card hidden>")
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:",*player.cards,sep='\n')
    
def show_all(player,dealer):    #for showing all the cards of the dealer and player
    print("\nDealer's Hand:",*dealer.cards,sep='\n')
    print("Dealer's Hand=",dealer.value)
    print("\nPlayer's Hand:",*player.cards,sep='\n')
    print("Player's Hand=",player.value)

def player_busts(player,dealer,chips):
    print("player busts!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("player wins!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("dealer busts!,player wins")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("dealer wins!")
    chips.lose_bet()
    
def push(player,dealer):
    print("dealer and player tie! It's a push.")


while True:
    
    deck=Deck()
    deck.shuffle()  #shuffling the deck
    playing=True
    
    player_hand=HumanPlayer()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())   #handing two cards to the player
    
    dealer_hand=HumanPlayer()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())   #handing two cards to the dealer
            
    pl_chips=int(input("enter the number of chips you would like to play with:"))
    player_chips = Chips(pl_chips)   
    
    take_bet(player_chips)  #ask the player to place a bet
    
    show_some(player_hand,dealer_hand)  #show of cards(1 card of dealer is hidden)
    
    while playing:  
        
        hit_or_stand(deck,player_hand)  #ask the player for a hit or stand
        
        show_some(player_hand,dealer_hand)  #show of cards(1 card of dealer is hidden) 
        
        if player_hand.value>21:  #If player's hand exceeds 21,human player busts
            player_busts(player_hand,dealer_hand,player_chips)
            break        

  
    if player_hand.value<=21: # If player hasn't busted,dealer will play
        
        while dealer_hand.value<player_hand.value:  #dealer keeps hitting until he surpasses player's hand or wins
            hit(deck,dealer_hand)

            show_all(player_hand,dealer_hand)   #all cards are shown
        
        #different winning scenarios
        if dealer_hand.value>21:
            dealer_busts(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value>player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value<player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)

        else:
            push(player_hand,dealer_hand)        
    
    print("\nPlayer's winnings stand at",player_chips.total)    #printing total chips of player
    
    new_game = input("Would you like to play another hand? Enter 'y' or 'n':")   #asking the player whether he/she wants to play a new game
    
    if new_game[0].lower()=='y':
        playing=True
        continue
    else:
        break









