# package: code/utils

#write in alternating colors in the console
def rainbow(string : str) :
    colors = ["\033[91m","\033[92m","\033[93m","\033[94m","\033[95m","\033[96m","\033[97m"]
    
    rainbow_string = ""
    
    for i in range(len(string)) :
        rainbow_string += colors[i % len(colors)] + string[i]
    
    return rainbow_string

from random import randint
def random(string : str) :
    """Randomly color each character in the string."""
    colors = ["\033[91m","\033[92m","\033[93m","\033[94m","\033[95m","\033[96m","\033[97m"]
    
    random_string = ""
    
    for i in range(len(string)) :
        random_string += colors[randint(0,len(colors)-1)] + string[i]
    
    return random_string