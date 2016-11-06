import pygame, colors
		
class ShapeRenderer(object):
	"""Renders simple shapes
	"""
	
	def __init__(self, surface):
		"""Constructor
		"""
		self.surface = surface
	
	def render_circle(self, pos, r, color=None):
		"""Draws a pygame circle
		"""
		pygame.draw.circle(self.surface, color, pos, r, 0)
	
	def render_rect(self, coords, color=None, alpha=None):
		"""Draws a pygame rectangle
		"""
		if alpha == None:
			pygame.draw.rect(self.surface, color, coords) # Draw a basic rectangle
		else:
			s = pygame.Surface((coords[2] - coords[0], coords[3] - coords[1])) # the size of the rect
			s.set_alpha(alpha)                           # alpha level
			s.fill(color)                                # this fills the entire surface
			self.surface.blit(s, (coords[0], coords[1])) # set the top-left coordinates

class Option(object):
	"""Minimal return data class
	"""
	def __init__(self, is_hovered):
		self.is_hovered = is_hovered

class OptionRenderer(object):
	"""Basically TextRenderer but this handles hovering automatically
	"""
	
	def __init__(self, surface, font, do_hover=True):
		"""Constructor
		"""
		self.font = font
		self.surface = surface
		self.do_hover = do_hover

	def render(self, text, pos, color=colors.MID_GRAY, hover_color=colors.WHITE, center=False):
		""" Renders an option
		"""
		rect = self._make_rect(text, pos, center)
		rend = self._do_rend(text, rect, color, hover_color)
		self.surface.blit(rend, rect)
		return Option(self._is_hovered(rect))

	def _do_rend(self, text, rect, color, hover_color):
		"""Rendering Imp'l
		"""
		return self.font.render(text, True, self._get_color(rect, color, hover_color))

	def _is_hovered(self, rect):
		"""Checks if the mouse is over the item
		"""
		return rect != None and rect.collidepoint(pygame.mouse.get_pos())
	
	def _get_color(self, rect, color, hover_color):
		"""Get's the color for item including hovering handling
		"""
		if self.do_hover and self._is_hovered(rect):
			return hover_color
		else:
			return color
	
	def _make_rect(self, text, pos, center):
		"""Makes the outline rectangle for the object
		"""
		rect = self._do_rend(text, None, (0,0,0), (0,0,0)).get_rect()
		if center:
			rect.center = pos
		else:
			rect.topleft = pos
		return rect
		
class Sprite(pygame.sprite.Sprite):
	"""Base class for custom sprites classes
	"""
	
	def __init__(self, x, y, file_name, use_alpha=False):
		"""C'tor
		"""
		# Init the parent class
		super(Sprite, self).__init__()
		
		# Load the image
		self._use_alpha = use_alpha
		self._change_image(file_name)
		
		# Store positional information
		self.x = x
		self.y = y
		self.rect.topleft = [x, y]
		
	def _change_image(self, file_name):
		"""Updates the image of the sprite
		"""
		# Update the image
		unconverted_image = pygame.image.load(file_name)
		self.image = unconverted_image.convert_alpha() if self._use_alpha else unconverted_image.convert()
		
		# Update the rect
		self.rect = self.image.get_rect()
		
	def is_hovered(self):
		return self.rect.collidepoint(pygame.mouse.get_pos())

class SpriteRenderer(object):
	"""Handlers rendering sprites
	"""
	def __init__(self, surface):
		"""C'tor
		"""
		self.surface = surface
		
	def render(self, sprite, convert_rect=None):
		"""Renders the sprite to the screen
		"""
		self.surface.blit(sprite.image, sprite.rect if convert_rect == None else convert_rect(sprite.rect))
		return sprite
