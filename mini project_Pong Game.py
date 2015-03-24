# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [2, 2] # ball speed(velocity)
    
    ball_vel[0] = random.randrange(120, 240)/60
    ball_vel[1] = random.randrange(60, 180)/60
   
    if direction == LEFT:
        ball_vel[0] = -ball_vel[0]
    ball_vel[1] = -ball_vel[1]
    

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints

    paddle1_vel = 0
    paddle2_vel = 0
    paddle1_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    paddle2_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    score1 = 0
    score2 = 0
    
    spawn_ball(RIGHT)
    

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    # When a ball meets top or bottom, a ball bounces back to the table
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    
    # When a ball touches the left paddle, a ball bounces back to the table calling
    # spawn_ball(RIGHT),while it touches the left gutter, opposite player scores.
    # To moderately increase the difficulty of the game, increase the velocity of
    # the ball by 10% each time it strikes a paddle.
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ball_pos[1] >= paddle1_pos and ball_pos[1] <= paddle1_pos + PAD_HEIGHT:
            ball_vel[0] = -1.1 * ball_vel[0]
            ball_vel[1] = 1.1 * ball_vel[1]
        else:
            score2 += 1
            spawn_ball(RIGHT)
            
    # When a ball touches the right paddle, a ball bounces back to the table calling
    # spawn_ball(LEFT),while it touches the right gutter, opposite player scores.        
    # To moderately increase the difficulty of the game, increase the velocity of
    # the ball by 10% each time it strikes a paddle.
    if ball_pos[0] >= ((WIDTH - PAD_WIDTH) - 1) -  BALL_RADIUS:
        if ball_pos[1] >= paddle2_pos and ball_pos[1] <= paddle2_pos + PAD_HEIGHT:
            ball_vel[0] = -1.1 * ball_vel[0]
            ball_vel[1] = 1.1 * ball_vel[1]
        else:
            score1 += 1
            spawn_ball(LEFT)
    
    # ball position   
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")    
    
    # update paddle's vertical position, keep paddle on the screen
    # Below 'first if' statements keeps two paddles on the screen
    # if paddles' positions go over the upper or bottom limits
    # set the paddle positions top(0) and bottom(HEIGHT-PAD_HEIGHT) respectively.
    if paddle1_pos >= 0 and paddle1_pos + PAD_HEIGHT <= HEIGHT:
        paddle1_pos += paddle1_vel
    elif paddle1_pos < 0:
        paddle1_pos = 0
    elif paddle1_pos + PAD_HEIGHT > HEIGHT:
        paddle1_pos = HEIGHT - PAD_HEIGHT
  

    if paddle2_pos >= 0 and paddle2_pos + PAD_HEIGHT <= HEIGHT:
        paddle2_pos += paddle2_vel
    elif paddle2_pos < 0:
        paddle2_pos = 0
    elif paddle2_pos + PAD_HEIGHT > HEIGHT:
        paddle2_pos = HEIGHT - PAD_HEIGHT

    
    # draw paddles  
    canvas.draw_polygon([[0, paddle1_pos], [0, paddle1_pos + PAD_HEIGHT]
                        , [PAD_WIDTH, paddle1_pos + PAD_HEIGHT], [PAD_WIDTH, paddle1_pos]],
                        1, "White", "White")
    canvas.draw_polygon([[WIDTH - PAD_WIDTH, paddle2_pos], [WIDTH - PAD_WIDTH, paddle2_pos + PAD_HEIGHT],
                        [WIDTH-1, paddle2_pos + PAD_HEIGHT],[WIDTH-1, paddle2_pos]],
                        1, "White", "White")
                                                                 
    
    # draw scores
    canvas.draw_text(str(score1), [150, 70], 60, 'White')
    canvas.draw_text(str(score2), [450, 70], 60, 'White')
        
def keydown(key):
    # When key pressed, its velocity is accelerates by 1(down) or -1(up)
    # 2 of paddle velocity is moderate. To move the paddle motion slower/faster 
    # decrease/increase the number.
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel += 2
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += 2
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= 2
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= 2

       
def keyup(key):
    # When key released, set the velocity '0', Otherwise, paddles keep moving up or down
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0

def button_handler():
    new_game()

    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', button_handler, 100)

# start frame
new_game()
frame.start()
