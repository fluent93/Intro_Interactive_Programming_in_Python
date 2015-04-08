# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
game_result = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank, open = True):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
            self.open = open
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        
        # draw card face or card back
        if self.open:
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        else:
            canvas.draw_image(card_back, (CARD_CENTER[0], CARD_CENTER[1]), CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        

            
class Hand:
    # Hand is the list of cards
    def __init__(self):
        self.card_list = []

    def __str__(self):
        cards_in_str = "" # return a string representation of a hand
        for i in range(len(self.card_list)):
            cards_in_str += str(self.card_list[i]) + " "
        return "Hand contains " + cards_in_str

    def add_card(self, card):
        self.card_list.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        for i in self.card_list:
            value += VALUES[i.get_rank()]
        
        for i in self.card_list:
            if i.get_rank() == 'A':
                if value + 10 <= 21:
                    return value + 10
                else:
                    return value
        return value
    
    # To decide the card's face or back, transfer this info to the card object
    def open(self):
        for i in self.card_list:
            i.open = True 
   
    def draw(self, canvas, pos):
    # draw a hand on the canvas, use the draw method for cards
        for i in range(len(self.card_list)):
            self.card_list[i].draw(canvas, pos)
            pos[0] += 100

            
class Deck:
    def __init__(self):
        self.card_list = [Card(x, y) for x in SUITS for y in RANKS]

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.card_list)

    def deal_card(self, open = True):
#        card = self.card_list.pop(-1)
#        card.open = open
#        return card	# deal a card object from the deck
        return self.card_list.pop(-1)
    
    def __str__(self):
        cards_in_str = ""
        for i in range(len(self.card_list)):
            cards_in_str += str(self.card_list[i]) + " "
        return "Deck contains "  + cards_in_str 


    
def deal():
    global outcome, game_result, in_play, playing_deck, player, dealer, score

    playing_deck = Deck()
    playing_deck.shuffle()
    player = Hand()
    dealer = Hand()
    player_card1 = playing_deck.deal_card()
    player_card2 = playing_deck.deal_card()
    dealer_card1 = playing_deck.deal_card()
    dealer_card1.open = False
    dealer_card2 = playing_deck.deal_card()

    player.add_card(player_card1)
    player.add_card(player_card2)
    dealer.add_card(dealer_card1)
    dealer.add_card(dealer_card2)
    outcome = "Hit or Stand?"
    game_result = ""

    # if another deal button clicked in the middle of in play, player lost
    if in_play:
        score -= 1
        game_result = "You lose with another deal click"
        outcome = "New deal?"
        in_play = False
        dealer.open()
        return
    in_play = True        
    

def hit():
    # if the hand is in play, hit the player
    global score, dealer, player, in_play, outcome, game_result
    player.add_card(playing_deck.deal_card())
    
    # if busted, assign a message to outcome, update in_play and score
    if player.get_value() > 21:
        game_result = "You went bust and lose"
        outcome = "New deal?"
        score -= 1
        
        dealer.open()
        in_play = False
   


def stand():
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more 
    global score, dealer, in_play, game_result, outcome
    
    while dealer.get_value() < 17:
        dealer_card = playing_deck.deal_card()
        dealer.add_card(dealer_card)
    if dealer.get_value() > 21:
        score += 1
        game_result = "Dealer busted and You win"
        outcome = "New deal?"
 
    else:
        if player.get_value() <= dealer.get_value():
            game_result = "You lose"
            outcome = "New deal?"
            score -= 1
        else:
            game_result = "You win"
            outcome = "New deal?"
            score += 1
    dealer.open()
    in_play = False
        
   

# draw handler    
def draw(canvas):

    global outcome, player, dealer
    canvas.draw_text('Blackjack', [100, 80], 40, 'Blue', 'sans-serif')
    canvas.draw_text('Score  ' + str(score), [450, 80], 30, 'Black', 'sans-serif')
    canvas.draw_text('Dealer', [30, 150], 30, 'Black', 'sans-serif')
    canvas.draw_text('Player', [30, 400], 30, 'Black', 'sans-serif')
    canvas.draw_text(game_result, [250, 150], 27, 'Black', 'sans-serif')
    canvas.draw_text(outcome, [250, 400], 27, 'Black', 'sans-serif')

    dealer.draw(canvas, [30, 170])
    player.draw(canvas, [30, 430])
    # if in play, dealer's hole(first) card is face down
#    if in_play:
#        canvas.draw_image(card_back, (CARD_CENTER[0], CARD_CENTER[1]), CARD_SIZE, [30 + CARD_CENTER[0], 170 + CARD_CENTER[1]], CARD_SIZE)   
#

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()