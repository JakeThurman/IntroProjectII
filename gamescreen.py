import pygame, sys, colors, fonts
from pygame.locals import *
from rendering import *
from screen import Screen

class Card(Sprite):
	def __init__(self, x, y, card_val, card_suit):
		super(Logo, self).__init__(x, y, "images/{0}{1}.png".format(card_val, card_suit))

class GameScreen(Screen):
	"""Renderers Game Screen
	"""

	def __init__(self, surface, screen_size, screen_manager):
		"""Constructor
		"""
		# init parent class
		super(GameScreen, self).__init__()
		
		# Create dependencies
		self.shape_renderer = ShapeRenderer(surface)
		self.sprite_renderer = SpriteRenderer(surface)
		self.option_renderer = OptionRenderer(surface, fonts.OPEN_SANS())
		
		# Store settings
		self._screen_size = screen_size
		self._screen_manager = screen_manager
		
	def handle_click(self):
		pygame.quit()
		sys.exit()
	
	def handle_key_up(self, key):
		"""Handles a key up event by begining the game
		"""
		# Close the game if escape is pressed
		if key == K_ESCAPE:
			pygame.quit()
			sys.exit()

	def render(self, refresh_time):
		"""Renderers the screen 
		"""
		# Set the backgroud to white
		self.shape_renderer.render_rect((0, 0, self._screen_size[0], self._screen_size[1]), color=colors.DARK_GRAY)
		
		
		