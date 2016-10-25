from pygame import font

font.init()

LINK_TEXT_SIZE = 25

def OPEN_SANS(size=LINK_TEXT_SIZE):
	return font.Font("fonts\OpenSans-Regular.ttf", size)