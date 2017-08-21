import socket
import pygame
from game import game
import math
from player import Player
from constants import Resources
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep
import random

BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
LIGHTGRAY = (200, 200, 200)
GRAY = (70, 70, 70)
BROWN = (206, 183, 99)

def coord_hexagon(radius, position):
		return [[position[0], position[1]-2*radius/math.sqrt(3)],
                [position[0]+radius, position[1]-radius/math.sqrt(3)],
                [position[0]+radius, position[1]+radius/math.sqrt(3)],
				[position[0], position[1]+2*radius/math.sqrt(3)],
				[position[0]-radius, position[1]+radius/math.sqrt(3)],
                [position[0]-radius, position[1]-radius/math.sqrt(3)]]

class Katan(ConnectionListener):
	def __init__(self):
		pass
		pygame.init();
		self.width, self.height, self.radius = 1000, 750, 60
		self.screen = pygame.display.set_mode((self.width, self.height))
		wood = pygame.image.load('wood_final.png').convert_alpha()
		brick = pygame.image.load('brick_final.png').convert_alpha()
		sheep = pygame.image.load('sheep_final.png').convert_alpha()
		wheat = pygame.image.load('wheat_final.png').convert_alpha()
		stone = pygame.image.load('stone_final.png').convert_alpha()
		desert = pygame.image.load('desert_final.png').convert_alpha()
		self.board = pygame.image.load('board.png').convert_alpha()
		numbers = []
		for i in range(2, 13):
			numbers.append(pygame.image.load(str(i) + '.png').convert_alpha())
		self.tiles = dict(zip([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], numbers))
		self.images = {Resources.WOOD:wood, Resources.BRICK:brick, Resources.SHEEP:sheep,
					   Resources.WHEAT:wheat, Resources.STONE:stone, Resources.DESERT:desert}
		self.catan = game(4, self.radius, [self.width/2-30, self.height/2], ["raw_input()", "raw_input()", "raw_input()", "raw_input()"])

		self.hello = pygame.display.get_surface()
		self.new = pygame.Surface((1000, 750))


		#This is some weird 3D magic, don't mess with it plz :)
		'''for y in range (-self.height//2, self.height//2):
			for x in range (-self.width//2, self.width//2):
				horizon = 50 #adjust if needed
				fov = 10

				px = x;
				py = fov;
				pz = y + horizon

				if pz != 0:
					#projection
					sx = px / pz
					sy = py / pz;

					scaling = 10; #adjust if needed, depends of texture size
					if round(sx * scaling) >= -self.width//2 and round(sx * scaling) < self.width//2 and round(sy * scaling) >= -self.height//2 and round(sy * scaling) < self.height//2:
						color = hello.get_at((round(sx * scaling) + self.width//2, round(sy * scaling) + self.height//2))
						self.new.set_at((x+self.width//2, y+self.height//2), color)'''

		#self.screen.fill(0)
		#self.screen.blit(self.new, [0, 0])

		pygame.display.set_caption("Katan")
		self.clock = pygame.time.Clock()
		print(pygame.display.list_modes())
		self.Connect()

	def drawBoard(self):
			self.screen.fill(GRAY)
			self.screen.blit(self.board, [69, 22])
			for i in range(19):
				self.screen.blit(self.images[self.catan.board[i].resource], [self.catan.pixelLoc[i+1][0]-self.radius, self.catan.pixelLoc[i+1][1]-self.radius*2/math.sqrt(3)])
				self.screen.blit(self.tiles[self.catan.board[i].number], [self.catan.pixelLoc[i+1][0]-14, self.catan.pixelLoc[i+1][1]-14])
			for i in range(19):
				pygame.draw.polygon(self.screen, BROWN, coord_hexagon(self.radius, self.catan.pixelLoc[i+1]), 4)

			self.hello = pygame.display.get_surface()
			self.new = pygame.Surface((1000, 750))

			pygame.draw.rect(self.screen, LIGHTGRAY, (10, 100, 130, 40))
			self.diceButton = pygame.Rect(10, 100, 130, 40)
			myfont_die = pygame.font.SysFont(None, 35)
			text = myfont_die.render('Roll Die', 1, WHITE)
			self.screen.blit(text, [30, 110])

			pygame.draw.rect(self.screen, LIGHTGRAY, (765, 88, 130, 40))
			self.buildButton = pygame.Rect(765, 88, 130, 40)
			myfont_build = pygame.font.SysFont(None, 35)
			text = myfont_build.render('Build', 1, WHITE)
			self.screen.blit(text, [800, 96])

			pygame.draw.rect(self.screen, LIGHTGRAY, (765, 30, 130, 40))
			self.tradeButton = pygame.Rect(765, 50, 130, 40)
			myfont_trade = pygame.font.SysFont(None, 35)
			text = myfont_trade.render('Trade', 1, WHITE)
			self.screen.blit(text, [800, 38])


	def drawCards(self, player):
		woolCard = pygame.image.load('wool.png').convert_alpha()
		woodCard = pygame.image.load('wood.png').convert_alpha()
		brickCard = pygame.image.load('brick.png').convert_alpha()
		stoneCard = pygame.image.load('stone.png').convert_alpha()
		wheatCard = pygame.image.load('wheat.png').convert_alpha()
		cardImages = [woodCard, brickCard, woolCard, wheatCard, stoneCard]
		#cardBack = pygame.image.load('cardBack.png').convert_alpha()
		width, height = pygame.display.get_surface().get_size()
		myfont = pygame.font.SysFont(None, 30)
		y = 10
		for p in self.catan.players:
			if p != player:
				label = myfont.render(str(p.name) + ": " + str(p.num_cards), 1, WHITE)
				self.screen.blit(label, [10, y])
				y += 25

		"""
		y = 10
		for x in range(7):
			pygame.draw.rect(self.screen, LIGHTGRAY, (width - 77, y, 61, 97))
			y += 95
		"""

		self.card_coord = [pygame.Rect(width - 77, 10, 61, 97), pygame.Rect(width - 77, 105, 61, 97), pygame.Rect(width - 77, 200, 61, 97),
						   pygame.Rect(width - 77, 295, 61, 97), pygame.Rect(width - 77, 390, 61, 97), pygame.Rect(width - 77, 485, 61, 97),
						   pygame.Rect(width - 77, 580, 61, 97)]

		y = 10
		hand_number = 0
		for r in player.cards:
			image = cardImages[r-1]
			for n in range(player.cards[r]):
				self.screen.blit(image, [width - 75, y])
				player.hand[hand_number] = r
				hand_number += 1
				y += 95

	def select_card(self, player, num):
		pygame.draw.rect(self.screen, WHITE, self.card_coord[num])
		player.selected_cards.append(player.hand[num])

	def build_city(self, pos):
		blue_city = pygame.image.load('bluecity'.png').convert_alpha()
		self.cities.append(pos)
		self.screen.blit()

	def update(self):
		#sleep to make the game 60 fps
		self.clock.tick(60)
		connection.Pump()
		self.Pump()

		#clear the screen
		self.screen.fill(0)
		self.drawBoard()
		self.screen.blit(self.hello, [0, 0])
		self.drawCards(self.catan.players[1])

		#print(self.catan.players[1].selected_cards)

		#blit dice roll
		myfont = pygame.font.SysFont(None, 40)
		roll = myfont.render(str(self.catan.roll), 1, WHITE)
		self.screen.blit(roll, [35, 155])

		for event in pygame.event.get():
			#quit if the quit button was pressed
			if event.type == pygame.QUIT:
				exit()
			pos = pygame.mouse.get_pos()
			if event.type == pygame.mouse.get_pressed()[0]:
				#roll dice
				if self.diceButton.collidepoint(pos):
					self.roll_die()
					self.screen.blit(roll, [35, 155])
				#select cards for trading or building
				for coord in range(7):
					if self.card_coord[coord].collidepoint(pos):
						self.select_card(self.catan.players[1], coord)
			if event.type == pygame.mouse.get_pressed()[1]:
				self.build_city()


		#update the screen
		pygame.display.flip()

	def roll_die(self):
		self.catan.roll = (random.randint(1, 6), random.randint(1, 6))


letsgo = Katan()
while 1:
    letsgo.update()
