#!/usr/bin/env python
"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation, 
follow along in the tutorial.
"""


#Import Modules
import os, pygame, sys
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'


#functions to create our resources
def load_image(name, colorkey=None):
	fullname = os.path.join('data', name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error, message:
		print 'Cannot load image:', fullname
		raise SystemExit, message
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	return image, image.get_rect()

def load_sound(name):
	class NoneSound:
		def play(self): pass
	if not pygame.mixer or not pygame.mixer.get_init():
		return NoneSound()
	fullname = os.path.join('data', name)
	try:
		sound = pygame.mixer.Sound(fullname)
	except pygame.error, message:
		print 'Cannot load sound:', fullname
		raise SystemExit, message
	return sound

#classes for our game objects
class Square(pygame.sprite.Sprite):
	def __init__(self, x, y, b, s):
		pygame.sprite.Sprite.__init__(self)
		self.isbrick = b
		self.issand = s
		self.x = x
		self.y = y

		if(b and s):
			self.image = pygame.image.load("sprites/bricksand.png").convert_alpha()
			self.rect = pygame.Rect(x*24, y*24, self.image.get_rect().width, self.image.get_rect().height)
		elif(b):
			self.isbrick = True
			self.image = pygame.image.load("sprites/brick.png").convert_alpha()
			self.rect = pygame.Rect(x*24, y*24, self.image.get_rect().width, self.image.get_rect().height)
		elif(s):
			self.issand = True
			self.image = pygame.image.load("sprites/sand.png").convert_alpha()
			self.rect = pygame.Rect(x*24, y*24, self.image.get_rect().width, self.image.get_rect().height)
		
class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("Sprites/player_right.PNG").convert_alpha()
		self.rect = pygame.Rect(0, 672, self.image.get_rect().width, self.image.get_rect().height)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		
		self.pos = 0
		self.maxPos = 19
		
		self.score = 0
		self.bank = 0
		self.mult = 1
	
	def move(self, dir):
		if dir > 0 and self.pos<self.maxPos:
			self.pos+=1
			self.rect = self.rect.move(self.image.get_rect().width,0)
			#print "yay"
		elif dir < 0 and self.pos > 0:
			self.pos-=1
			self.rect = self.rect.move(-1*self.image.get_rect().width,0)
			#print "yeah"
	
	def drill(self, grid):
		if grid[self.pos][27].isbrick:
			self.mult=1
			self.bank-=1
		if grid[self.pos][27].issand:
			grid[self.pos][27]=Square(self.pos, 27, False, False)
			drillCol(self.pos, grid)

def drillCol(x, grid):
	y=len(grid[x])-1
	if x >=0 or x<20:
		for i in range(0, y):
			if grid[x][y-1-i].issand:
				grid[x][y-i]=Square(x, y-i, grid[x][y-1-i].isbrick, grid[x][y-1-i].issand)
			else:
				grid[x][y-i]=Square(x, y-i, False, False)
				return

def moveGrid(grid):
	l=len(grid[0])-1
	for x in range(0, len(grid)):
		for y in range(0, len(grid[x])-1):
			if grid[x][l-1-y].issand or grid[x][l-1-y].isbrick:
				if not(grid[x][l-y].issand or grid[x][l-y].isbrick):
					grid[x][l-y]=Square(x, l-y, grid[x][l-1-y].isbrick, grid[x][l-1-y].issand)
					grid[x][l-1-y]=Square(x, l-1-y, False, False)
		
def main():
	"""this function is called when the program starts.
	   it initializes everything it needs, then runs in
	   a loop until the function returns."""
#Initialize Everything
	pygame.init()
	screen = pygame.display.set_mode((480, 696))
	pygame.display.set_caption('Mr. Flatland!')
	pygame.mouse.set_visible(0)

#Create The Backgound
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))
	backgroundImg = pygame.image.load('data/sky.png')
	backgroundImgRect = backgroundImg.get_rect()
	
#Put Text On The Background, Centered
	if pygame.font:
		font = pygame.font.Font(None, 36)
		text = font.render("Mr. Flatland Rocks!", 1, (10, 10, 10))
		textpos = text.get_rect(centerx=background.get_width()/2)
		backgroundImg.blit(text, textpos)

#Display The Background
	screen.blit(background, (0,0))
	screen.blit(backgroundImg, backgroundImgRect)
	pygame.display.flip()
	
#Prepare Game Objects
	clock = pygame.time.Clock()
	player = Player()
	allsprites = pygame.sprite.RenderPlain((player))
	
	seconds = 0

	#Game Setup
	#Empty space
	grid = []
	for x in range(0,20):
		grid.append([])
		for y in range(0,28):
			grid[x].append(Square(x,y,False,False))

	#Sand
	for x in range(0,20):
		for y in range(20,28):
			grid[x][y] = Square(x,y,False,True)

	for x in range(0,10):
		for y in range(0,5):
			grid[x][y] = Square(x,y,True,True)
				
	for x in range(10,20):
		for y in range(15,20):
			grid[x][y] = Square(x,y,True,False)

#Main Loop
	while 1:
		clock.tick()
		
		if seconds < pygame.time.get_ticks()/1000.0:
			seconds+=1
			#put code here that happens every second!
			moveGrid(grid)

	#Handle Input Events
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					return
				elif event.key == pygame.K_RIGHT:
					player.move(1)
					#print "right"
				elif event.key == pygame.K_LEFT:
					player.move(-1)
					#print "left"
				elif event.key == pygame.K_SPACE:
					player.drill(grid)
#			elif event.type == KEYUP:
#				if event.key == pygame.K_RIGHT:
#					player.move(1)
#					#print "right"
#				elif event.key == pygame.K_LEFT:
#					player.move(-1)
#					#print "left"

		allsprites.update()

	#Draw Everything
		screen.blit(background, (0,0))
		screen.blit(backgroundImg, backgroundImgRect)

		for x in range(0,20):
			for y in range(0,28):
				if(grid[x][y].issand or grid[x][y].isbrick):
					screen.blit(grid[x][y].image, grid[x][y].rect)

		allsprites.draw(screen)
		pygame.display.flip()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()