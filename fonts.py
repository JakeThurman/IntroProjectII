import random
from pygame import font

font.init()

LINK_TEXT_SIZE = 25

def random_font(size=LINK_TEXT_SIZE):
	return random_font_factory()(size)

def random_font_factory():
	my_font = random.choice(("OpenSans-Regular", "OpenSans-Regular", "OpenSans-Regular", "mypager", "stocky"))
	
	def font_factory(size=LINK_TEXT_SIZE):
		return font.Font("fonts\\" + my_font + ".ttf", size)
	
	return font_factory