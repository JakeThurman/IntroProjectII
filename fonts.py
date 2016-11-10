import random
from pygame import font

font.init()

LINK_TEXT_SIZE = 25

def random_font(size=LINK_TEXT_SIZE):
	choices = ["OpenSans-Regular", "80db", "citycontrasts", "fleck", "Leadcoat", "milit", "mypager", "stocky"]
	return font.Font("fonts\\" + random.choice(choices) + ".ttf", size)