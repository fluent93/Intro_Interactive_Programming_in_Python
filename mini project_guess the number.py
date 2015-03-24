# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

secret_number = 0
remaining_guess = 0
num_range = 0


# helper function to start and restart the game
def new_game():
    if num_range == 1000:
        range1000()
    else:
        range100()    


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global remaining_guess
    global secret_number
    global num_range

    remaining_guess = 7
    secret_number = random.randrange(0, 100)
    
    print "New game. Range is from 0 to 100"
    print "Number of remaining guesses is ", remaining_guess
    print

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global remaining_guess
    global secret_number
    global num_range
    num_range = 1000
    remaining_guess = 10
    secret_number = random.randrange(0, 1000)
    
    print "New game. Range is from 0 to 1000"
    print "Number of remaining guesses is ", remaining_guess
    print
    
    
def input_guess(guess):
    guess_int = int(guess)
    print "Guess was ", guess_int
    
    global secret_number
    global remaining_guess
    global num_range
    
    remaining_guess = remaining_guess - 1
    print "Number of remaining guesses is ", remaining_guess
    
    if remaining_guess != 0:
        if guess_int > secret_number:
            print "Lower!"
            print
        elif guess_int < secret_number:
            print "Higher!"
            print
        else:
            print "Correct!"
            print
            new_game()
    else:        
        if guess_int == secret_number:
            print "Correct!"
            print
            new_game()
        else:
            print "You ran out of guesses. The number was ", secret_number 
            print
            new_game()
            return
 
              
# create frame
f = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements and start frame
f.add_button("Range is [0, 100)", range100, 200)
f.add_button("Range is [0, 1000)", range1000, 200)
f.add_input("Enter a guess", input_guess, 200)
f.start()

# call new_game 
new_game()