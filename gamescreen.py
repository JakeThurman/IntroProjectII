import pygame, sys, colors, fonts, random
from pygame.locals import *
from rendering import *
from screen import Screen

# Contants
CARD_WIDTH = 71

_img_cache = {}
def get_card_sprite(x, y, card_id):
	key = (x, y, card_id)
	
	if not key in _img_cache:
		_img_cache[key] = CardImg(x + random.randint(-3, 3), y, card_id)
	
	return _img_cache[key]

class CardImg(Sprite):
	def __init__(self, x, y, card_id):
		super(CardImg, self).__init__(x, y, "images/{0}.png".format(card_id.lower()))
		
class PlayAgainScreen(Screen):
	"""Asks the user if they wish to play again
	"""

	def __init__(self, surface, screen_size, screen_manager, winner_is_player1, winner_score):
		"""Constructor for the Play Again Screen
		"""		
		# init parent class
		super(PlayAgainScreen, self).__init__()
		
		# Create dependencies
		self.shape_renderer = ShapeRenderer(surface)
		self.option_renderer = OptionRenderer(surface, fonts.OPEN_SANS())
		self.header_renderer = OptionRenderer(surface, fonts.OPEN_SANS(30))
		
		# Store config
		self._winner_is_player1 = winner_is_player1
		self._winner_score = winner_score
		
		# Store settings
		self._screen_size = screen_size
		self._screen_manager = screen_manager
		
	def handle_click(self):
		# Play again if the user clicks Yes
		if self.yes_bttn.is_hovered:
			self._play_again()
		# Quit if the user clicks No
		elif self.no_bttn.is_hovered:
			pygame.quit()
			sys.exit()
	
	def _play_again(self):
		self._screen_manager.set(GameScreen)
	
	def handle_key_up(self, key):
		"""Handles a key up event by begining the game
		"""
		# Close the game if escape is pressed (on the 'N' key)
		if key == K_ESCAPE or key == K_n:
			pygame.quit()
			sys.exit()
		# Play again on 'Y' key pressed
		elif key == K_y:
			self._play_again()
			
	def render(self, refresh_time):
		"""Renderers the screen 
		"""
		# Set the backgroud to white
		self.shape_renderer.render_rect((0, 0, self._screen_size[0], self._screen_size[1]), color=colors.DARK_GRAY, alpha=40)
		
		# Render the text on the screen
		ss = self._screen_size
		
		winner_msg = ("Player 1 Wins!" if self._winner_is_player1 else "Player 2 Wins!") + " ({0} points)".format(self._winner_score)
		self.header_renderer.render(winner_msg, (ss[0]/10, ss[1]/10), color=colors.WHITE)
		
		self.header_renderer.render("Play Again?", (ss[0]/10, (ss[1]/10) * 3), color=colors.WHITE)
		
		self.yes_bttn = self.option_renderer.render("Yes Please!",   (ss[0]/10, (ss[1]/10) * 4), color=colors.LIGHT_GRAY)
		self.no_bttn =  self.option_renderer.render("No. I'm Done.", (ss[0]/10, (ss[1]/10) * 5), color=colors.LIGHT_GRAY)

class GameState:
	DECK_SPLIT = 0
	GAME = 1
	GAME_OVER = 2
	
class GameScreen(Screen):
	"""Renderers Game Screen
	"""

	def __init__(self, surface, screen_size, screen_manager):
		"""Constructor for the game screen
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
				
		# the deck of cards the game is played with.
		#  Used cards will be discarded into the deck
		#  The string at index 0 of each item is the name of that card's image
		#  The number at index 1 of each item is that card's value
		self._deck = [
			["as", 14], ["2s", 2], ["3s", 3], ["4s", 4], ["5s", 5], ["6s", 6],
			["7s", 7], ["8s", 8], ["9s", 9], ["10s", 10], ["js", 11], ["qs", 12], ["ks", 13],
			
			["ah", 14], ["2h", 2], ["3h", 3], ["4h", 4], ["5h", 5], ["6h", 6],
			["7h", 7], ["8h", 8], ["9h", 9], ["10h", 10], ["jh", 11], ["qh", 12], ["kh", 13],
			
			["ac", 14], ["2c", 2], ["3c", 3], ["4c", 4], ["5c", 5], ["6c", 6],
			["7c", 7], ["8c", 8], ["9c", 9], ["10c", 10], ["jc", 11], ["qc", 12], ["kc", 13],
			
			["ad", 14], ["2d", 2], ["3d", 3], ["4d", 4], ["5d", 5], ["6d", 6],
			["7d", 7], ["8d", 8], ["9d", 9], ["10d", 10], ["jd", 11], ["qd", 12], ["kd", 13]
		]
		
		# Shuffle our beautiful new deck
		random.shuffle(self._deck)
				
		# Set Initial State
		self._state = GameState.DECK_SPLIT
		self._should_make_war = False
		self._player_1_won_turn = None
		
		# 
		self._deck_split_timer = 0
		self._war_timer = 0
		
		self.player_1_deck = []
		self.player_2_deck = []
		self.player_1_battlefield = []
		self.player_2_battlefield = []
		
		self.player_1_score = 0
		self.player_2_score = 0
		
		# Holds the cards that should be kept facing 
		#  down as they were laid as part of a war
		self._war_casualties = []
		
	def handle_click(self):
		if self._state == GameState.GAME_OVER:
			self._on_game_end()
		elif self._state == GameState.GAME:
			self._take_turn()
		
	def _take_turn(self):
		if self._should_make_war:
			# When the cards are a tied, we have a war
			# Both players draw 3 cards, and then check who won.
			# Also reset the war flag
			self._should_make_war = False
			self._war_timer = 0
			self._draw_card(is_war_casualty=True)
			self._draw_card(is_war_casualty=True)
			self._draw_card(is_war_casualty=True)
			self._find_turn_champ(from_a_war=True)
		else:
			self._draw_card(is_war_casualty=False)
			self._find_turn_champ(from_a_war=False)
		
	def _draw_card(self, is_war_casualty):
		if self._state == GameState.GAME_OVER:
			return
	
		# display player 1's next card
		p1_card = self.player_1_deck.pop(0)
		self.player_1_battlefield.append(p1_card)
		
		# display player 2's next card
		p2_card = self.player_2_deck.pop(0)
		self.player_2_battlefield.append(p2_card)
		
		# Handle the case that this is a war casualty,
		#  and we need to record that the card should be 
		#  drawn face down.
		if is_war_casualty:
			self._war_casualties.append(p1_card)
			self._war_casualties.append(p2_card)
		
		# stop the game if we run out of cards
		if len(self.player_1_deck) == 0 or len(self.player_2_deck) == 0:
			self._state = GameState.GAME_OVER
			
	def _find_turn_champ(self, from_a_war):
		player_1_card = self.player_1_battlefield[len(self.player_1_battlefield)-1]
		player_2_card = self.player_2_battlefield[len(self.player_2_battlefield)-1]
		
		# Player 1 wins the skirmish
		if(player_1_card[1] > player_2_card[1]):
			self.player_1_score += player_1_card[1]
			self._player_1_won_turn = True
		
		# Player 2 wins the skirmish
		elif(player_1_card[1] < player_2_card[1]):
			self.player_2_score += player_2_card[1]
			self._player_1_won_turn = False
		
		# The Players have tied
		elif not from_a_war:
			self._should_make_war = True
			self._player_1_won_turn = None
	
	def _on_game_end(self):		
		winner_is_player1 = self.player_1_score > self.player_2_score
		winner_score = self.player_1_score if winner_is_player1 else self.player_2_score
		self._screen_manager.set(lambda *args: PlayAgainScreen(*args, winner_is_player1=winner_is_player1, winner_score=winner_score))
	
	def handle_key_up(self, key):
		"""Handles a key up event by begining the game
		"""
		# Close the game if escape is pressed
		if key == K_ESCAPE:
			pygame.quit()
			sys.exit()
			
	def _render_card_set(self, battlefield, start_pos, draw_only_card_backs=False, offset=8):
		for i in range(0, len(battlefield)):
			card = battlefield[i]
			card_type = card[0]
			if draw_only_card_backs or card in self._war_casualties:
				card_type = "back"
			
			img = get_card_sprite(start_pos[0], start_pos[1] + (i * offset), card_type)
			self.sprite_renderer.render(img)
			
	def _handle_time(self, refresh_time):
		self._deck_split_timer += refresh_time
		
		# Split the deck after a small delay	
		if self._state == GameState.DECK_SPLIT and self._deck_split_timer > 250:
			self.player_1_deck.append(self._deck.pop(0))
			self.player_2_deck.append(self._deck.pop())
			
			# Move to the next state if the deck is cleared
			if len(self._deck) == 0:
				self._state = GameState.GAME
				
		# Handle a "war" delay
		if self._should_make_war:
			self._war_timer += refresh_time
			
			if self._war_timer > 500:
				self._take_turn()
	
	def render(self, refresh_time):
		"""Renderers the screen 
		"""	
		self._handle_time(refresh_time)
		
		# Set the backgroud to white
		self.shape_renderer.render_rect((0, 0, self._screen_size[0], self._screen_size[1]), color=colors.DARK_GRAY)
		
		# Shortcut named variable
		ss = self._screen_size
		
		# Render the initial deck
		self._render_card_set(self._deck, (ss[0]/2 - CARD_WIDTH/2, ss[1]/6), offset=2.75, draw_only_card_backs=True)
	
		if self._state == GameState.GAME:
			# Tell the players how to play if the game is still going
			self.option_renderer.render("Click to take a turn!", (ss[0]/25, ss[1] - ss[1]/10), color=colors.MID_GRAY, hover_color=colors.MID_GRAY)
		
			if self._should_make_war:
				# Alert when there is a war going on
				self.option_renderer.render("WAR TIME", (ss[0]/2, ss[1]/2), color=colors.LIGHT_GRAY, hover_color=colors.LIGHT_GRAY, center=True)
				
			if self._player_1_won_turn != None:
				# Alert the user of who won each turn
				self.option_renderer.render("WINNER", (ss[0]/4 if self._player_1_won_turn else ss[0]-ss[0]/4, ss[1]/20), color=colors.LIGHT_GRAY, hover_color=colors.LIGHT_GRAY, center=True)
		
		if self._state == GameState.GAME_OVER:
			# Tell the players when the game is over
			self.option_renderer.render("Game Over!", (ss[0]/2, ss[1]/2), color=colors.LIGHT_GRAY, center=True)
			
		# Draw the player cards
		self._render_card_set(self.player_1_battlefield, (ss[0]/4, ss[1]/6))
		self._render_card_set(self.player_2_battlefield, (ss[0] - ss[0]/4 - CARD_WIDTH, ss[1]/6))
	
		# Print the score above the battlefield
		self.option_renderer.render("Player 1 ({0} points)".format(self.player_1_score), (ss[0]/4, ss[1]/10), color=colors.WHITE, center=True)
		self.option_renderer.render("Player 2 ({0} points)".format(self.player_2_score), (ss[0] - ss[0]/4, ss[1]/10), color=colors.WHITE, center=True)
				
		# Draw the cards in the player's hand
		self._render_card_set(self.player_1_deck, (ss[0]/12, ss[1]/6), draw_only_card_backs=True, offset=5)
		self._render_card_set(self.player_2_deck, (ss[0] - ss[0]/12 - CARD_WIDTH, ss[1]/6), draw_only_card_backs=True, offset=5)
