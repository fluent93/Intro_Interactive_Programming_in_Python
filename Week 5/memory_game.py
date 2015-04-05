# implementation of card game - Memory

import simplegui
import random

# initialize global variables. pair_first_idx, pair_second_idx to store the index of 
# each of the two cards. All 16 cards are initialized as 'False' facing down(unexposed)
def new_game():
    global whole_lst, state, exposed, pair_first_idx, pair_second_idx, counter
    counter = 0
    label.set_text("Turns = 0")
    pair_first_idx = 0
    pair_second_idx = 0
    state = 0
    lst1 = [x for x in range(8)]
    lst2 = [y for y in range(8)]
    whole_lst = lst1 + lst2 
    random.shuffle(whole_lst)
    exposed = [False, False, False, False, False, False, False, False, False, 
               False, False, False, False, False, False, False]

     
# define event handlers
def mouseclick(pos):
    global whole_lst, pos_index, state, exposed, pair_first_idx, pair_second_idx, counter
    pos_index = pos[0] / 50 # mouseclick index
    counter += 1
    label.set_text("Turns = " + str(counter))
    
    if state == 0:
        pair_first_idx = pos_index
        exposed[pair_first_idx] = True
        state = 1

    elif state == 1:
        # Ignore clicks on exposed cards with checking if mouse does not click any faced-up cards.
        # If it does, it gets out of 'for loop' and does not run even 'else clause'. Otherwise,
        # it runs 'else clause'
        for i in range(len(exposed)):
            if exposed[i]:
                if pos_index == i:
                    break
    
        else:
            pair_second_idx = pos_index
            exposed[pair_second_idx] = True
            state = 2

    else:
        # if the numbers of two exposed cards are the same, let them still open and the new card
        # is opened registering new pair_first_idx. If not, get both opened cards facing back down
        # and the new card is opened registering new pair_first_idx. Ignoring clicks on exposed cards
        # is the same logic as above.
        for i in range(len(exposed)):
            if exposed[i]:
                if pos_index == i:
                    break
        else:
                #if pos_index != pair_first_idx and pos_index != pair_second_idx:
            if whole_lst[pair_first_idx] != whole_lst[pair_second_idx]:
                exposed[pair_first_idx] = False
                exposed[pair_second_idx] = False
            pair_first_idx = pos_index
            exposed[pair_first_idx] = True
            state = 1

# cards are logically 50x100 pixels in size    
def draw(canvas):
    global whole_lst, card_width, exposed, hor_pos, index
    card_width = 50
    hor_pos = 0
    # if exposed(opened), draw the number, otherwise, draw the green deck
    for index in range(len(whole_lst)):
        if exposed[index]:
            canvas.draw_text(str(whole_lst[index]), [hor_pos + (index * card_width) + (50/4), 60], 30, 'White')
        else:
            canvas.draw_polygon([[hor_pos + (index * card_width), 0], [hor_pos + (index + 1) * card_width, 0], 
                                [hor_pos + (index + 1) * card_width, 100], [hor_pos + (index * card_width), 100]],
                                1, 'Black', 'Green')    
        index += 1

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()