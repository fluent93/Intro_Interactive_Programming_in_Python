import simplegui
import random

#empty CIPHER first, be a random dic later
CIPHER = {} 
LETTERS = "abcdefghijklmnopqrstuvwxyz" #all letters
message = ""

def init():
    letters_list = list(LETTERS)
    random.shuffle(letters_list)
    for ch in LETTERS:
        CIPHER[ch] = letters_list.pop()



def encode():
    emsg = ""
    for ch in message:
        emsg += CIPHER[ch]
    print message, "encodes to", emsg
    
    
def decode():
    dmsg = ""
    for ch in message:
        for key, value in CIPHER.items():
            if ch == value:
                dmsg += key
    print message, "decodes to", dmsg
    
    
    
def newmsg(msg):
    global message
    message = msg
    label.set_text(msg)
    
    
frame = simplegui.create_frame("Cipher", 2, 200, 200)
frame.add_input("Message:", newmsg, 200)
label = frame.add_label("", 200)
frame.add_button("Encode", encode)
frame.add_button("Decode", decode)

init()
frame.start()
