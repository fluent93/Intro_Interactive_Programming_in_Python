# template for "Stopwatch: The Game"

import simplegui
import time

# define global variables
global_integer = 0
attempt = 0
success = 0
mil_sec = 0
sec = 0
ten_sec = 0
min = 0

#This boolean value determines whether to update the score when the
#"Stop" button is pressed.When it's already stopped, it does not
#inclement the number of attemps and successes
running_check = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global mil_sec, sec, ten_sec, min
    mil_sec = t % 10
    sec = (t / 10) % 10
    ten_sec = (t / 100) % 6
    min = (t / 100) / 6

    return str(min) + ':' + str(ten_sec) + str(sec) + '.' + str(mil_sec)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()
    global running_check
    running_check = True

    
def stop():
    timer.stop()
    global running_check
    
    global attempt, success, mil_sec
    if running_check == True:
        attempt += 1
        if mil_sec == 0:
            success += 1
    running_check = False
    
def reset():
    timer.stop()
    global global_integer, attempt, success
    global_integer = 0
    attempt = 0
    success = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global global_integer
    global_integer += 1

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(global_integer),[70,130], 75, "White")
    canvas.draw_text(str(success) + '/' + str(attempt), [230, 30], 30, "Green")
    
# create frame
frame = simplegui.create_frame("Stopwatch", 300, 200)


# register event handlers
timer = simplegui.create_timer(100, timer_handler)
frame.set_draw_handler(draw_handler)
frame.add_button("Start", start, 50)
frame.add_button("Stop", stop, 50)
frame.add_button("Reset", reset, 50)


# start frame
frame.start()

# Please remember to review the grading rubric
