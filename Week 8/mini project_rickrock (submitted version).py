# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.3
friction = 0.03 #friction constant
started = False


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust: #thrustig spaceship image
            self.image_center[0] = 135
        else:
            self.image_center[0] = 45 #regular spaceship image
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.vel[0] *= (1 - friction)
        self.vel[1] *= (1 - friction) 
        self.pos[0] += self.vel[0]
        self.pos[0] %= WIDTH  #screen wrap using modular arithmetic
        self.pos[1] += self.vel[1]
        self.pos[1] %= HEIGHT  #screen wrap using modular arithmetic
        self.angle += self.angle_vel

        if self.thrust:
            self.vel[0] += angle_to_vector(self.angle)[0]
            self.vel[1] += angle_to_vector(self.angle)[1]
        
    def incre_angle_vel(self):
        self.angle_vel += .1 #angular velocity constant
        return self.angle_vel
    
    def decre_angle_vel(self):
        self.angle_vel -= .1  #angular velocity constant
        return self.angle_vel
    
    def thrust_sound(self):
        if self.thrust:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
 
    def shoot(self):
        a_missile_pos = [(self.pos[0] + angle_to_vector(self.angle)[0] * 45), (self.pos[1] + angle_to_vector(self.angle)[1] * 45)]
        a_missile_vel = [(self.vel[0] + angle_to_vector(self.angle)[0] * 4), (self.vel[1] + angle_to_vector(self.angle)[1] * 4)]
        a_missile = Sprite(a_missile_pos, a_missile_vel, self.angle, 0, missile_image, missile_info, missile_sound) 
        # missile added to the missile_group
        missile_group.add(a_missile)
 
    def key_down(self, key):
        if key == simplegui.KEY_MAP['left']:
            self.angle += self.decre_angle_vel()
        elif key == simplegui.KEY_MAP['right']:
            self.angle += self.incre_angle_vel()
        elif key == simplegui.KEY_MAP['up']:
            self.thrust = True
            self.thrust_sound()
        elif key == simplegui.KEY_MAP['space']:
            self.shoot()                     

    def key_up(self, key):
        if key == simplegui.KEY_MAP['left']:
            self.angle_vel = 0
        elif key == simplegui.KEY_MAP['right']:
            self.angle_vel = 0
        elif key == simplegui.KEY_MAP['up']:
            self.thrust = False
            self.thrust_sound()
            
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        # If Sprite instance is a missile, play its sound, otherwise, no sound
        # because rock instance has no sound parameter
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, 
                          self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[0] %= WIDTH  #screen wrap using modular arithmetic
        self.pos[1] += self.vel[1]
        self.pos[1] %= HEIGHT  #screen wrap using modular arithmetic
        
        # missile instance has its life span, otherwise there would be missiles all over 
        # the canvas
        self.age += 1
        if self.age >= self.lifespan:
            return True
        else:
            return False
        
        
    def collide(self, other_object):
        global lives
        if dist(self.pos, other_object.pos) <= self.radius + other_object.radius:
            return True
        else:
            return False
           
def draw(canvas):
    global time, lives, score, started, rock_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    splash_center = splash_info.get_center()
    splash_size = splash_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    # initial state is 'click to start with splash image'
    if not started:
        canvas.draw_image(splash_image, splash_center, splash_size, (WIDTH / 2, HEIGHT / 2), splash_size)
    canvas.draw_text('Lives', (50, 30), 20, 'White', 'sans-serif')
    canvas.draw_text(str(lives), (50, 55), 20, 'White', 'sans-serif')
    canvas.draw_text('Score', (700, 30), 20, 'White', 'sans-serif')
    canvas.draw_text(str(score), (700, 55), 20, 'White', 'sans-serif')

    # When lives is equal to '0', program is back to the initial state
    if lives == 0:
        score = 0
        lives = 3
        started = False
        soundtrack.pause()
        # destroy all rocks to make the program initial status
        for rock in rock_group:
            rock_group.discard(rock)
        
    
    # draw ship and sprites
    my_ship.draw(canvas)
    
    # update ship and sprites
    my_ship.update()

    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    group_collide(rock_group, my_ship)
    group_group_collide(rock_group, missile_group)
    
    
# timer handler that spawns a rock    
def rock_spawner():
    global time, rock_group, started
    if started:
        if len(rock_group) < 12: # set the limit of the number of rocks 12
            pos = [0, 0]
            vel = [10, 10]
            pos[0] = random.randrange(WIDTH)
            pos[1] = random.randrange(HEIGHT)
            vel[0] = random.random()
            vel[1] = random.random()
            new_rock = Sprite(pos, vel, 0, 0.02, asteroid_image, asteroid_info)
            
            # When a new rock spawned is too close to the ship, it is not created
            if dist(new_rock.pos, my_ship.pos) >= (new_rock.radius + my_ship.radius) + 30:
                rock_group.add(new_rock)
        angle_vel = random.random()

def process_sprite_group(group, canvas):
    global started
    remove_group = set()
    if started:
        for sprite in group:
            if sprite.update(): # when a missile is at its lifespan, it is terminated.
                remove_group.add(sprite)
            sprite.draw(canvas)
        group.difference_update(remove_group)
        
        
def group_collide(group, other_object):
    global lives
    remove_group = set()
    collision_flag = False
    for sprite in group:
        if sprite.collide(other_object):
            remove_group.add(sprite)
            collision_flag = True
            if other_object == my_ship:
                lives -= 1
    group.difference_update(remove_group)
    return collision_flag


def group_group_collide(group1, group2):
    global score
    first_group = group1
    for ele_gr1 in first_group:
        if group_collide(group2, ele_gr1):
            first_group.discard(ele_gr1)
            score += 10
    return score


def key_down(key):
    # forwardig to 'Ship' key handler
    my_ship.key_down(key)
        
def key_up(key):
    # forwardig to 'Ship' key handler
    my_ship.key_up(key) 
 
def click(pos):
    global started
    pos = [(WIDTH / 2 - splash_info.get_size()[0] / 2), (HEIGHT / 2 + splash_info.get_size()[1] / 2)]
    started = True
    soundtrack.rewind()
    soundtrack.play()

    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set()
missile_group = set()

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()