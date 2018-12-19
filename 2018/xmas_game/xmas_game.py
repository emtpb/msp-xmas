"""
 XMAS-Game
 Written for MSMP's X-Mas competition at UPB in Dec 2018
 (c) 2018 Fabian Bronner
"""

# Numpy
import numpy as np
# Matplotlib
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import matplotlib.patches as ptc
import matplotlib.animation as animation
import matplotlib.image as mpimg
# Matplotlib widgets
from matplotlib.widgets import Slider
from matplotlib.widgets import Button

# Classes
class Present:
	def __init__(self, ax, gameWidth):
		self.gameWidth = gameWidth
		self.x = np.random.random()*self.gameWidth
		self.y = 100+10
		self.width = 10
		self.height = 10
		self.speed = 0
		self.variation = 0
		self.catched = False
		self.missed = False
		self.frameCounter = 0
		self.colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 0.5, 0)]
		self.color = self.colors[np.random.randint(len(self.colors))]
		self.boxColor = (self.color[0]*0.7, self.color[1]*0.7, self.color[2]*0.7)
		self.addColor = (min(self.color[0]+0.3, 1), min(self.color[1]+0.3, 1), min(self.color[2]+0.3, 1))
		self.box = ptc.Rectangle((self.x, self.y), self.width, self.height, facecolor=self.boxColor)
		self.vLine = ptc.Rectangle((self.x+(0.4*self.width), self.y), self.width/5, self.height, facecolor=self.addColor)
		self.hLine = ptc.Rectangle((self.x, self.y+(0.4*self.width)), self.width, self.height/5, facecolor=self.addColor)

		ax.add_patch(self.box)
		ax.add_patch(self.vLine)
		ax.add_patch(self.hLine)
	def update(self):
		if self.catched == True:
			self.x = -1000
			self.speed = 0

		self.x -= self.variation * np.sin(self.frameCounter / 10)
		if self.x < 0 and self.catched == False:
			self.x = 0
		elif self.x > 90:
			self.x = 90
		self.y -= self.speed
		self.box.set_xy((self.x, self.y))
		self.vLine.set_xy((self.x+(0.4*self.width), self.y))
		self.hLine.set_xy((self.x, self.y+(0.4*self.width)))
		self.frameCounter += 1

	def getLeft(self):
		return self.x

	def getRight(self):
		return self.x+self.width

	def getTop(self):
		return self.y+self.height

	def getBottom(self):
		return self.y

	def getMiddleX(self):
		return self.x+(self.width/2)

	def getMiddleY(self):
		return self.y+(self.height/2)

	def setCatched(self, value):
		self.catched = value

	def setMissed(self, value):
		self.missed = value

	def isCatched(self):
		return self.catched

	def isMissed(self):
		return self.missed

	def start(self, speed, variation):
		self.speed = speed
		self.variation = variation

		self.x = np.random.random()*self.gameWidth

		self.color = self.colors[np.random.randint(len(self.colors))]
		self.boxColor = (self.color[0]*0.7, self.color[1]*0.7, self.color[2]*0.7)
		self.addColor = (min(self.color[0]+0.3, 1), min(self.color[1]+0.3, 1), min(self.color[2]+0.3, 1))

class PresentManager:
	def __init__(self, ax):
		self.presents = []
		# Setup presents
		for x in range(0, 100):
			present = Present(ax, 90)
			self.presents.append(present)
	def getPresents(self):
		return self.presents
	def update(self):
		for present in self.presents:
			present.update()
		if self.presentCountdown == 0 and self.presentCounter < self.numPresents:
			self.presentCountdown = self.framesBetweenPresents
			self.presents[self.presentCounter].start(0.5+(np.random.random()*self.maxSpeed), self.variation)
			self.presentCounter += 1
		else:
			self.presentCountdown -= 1
	def start(self, framesBetweenPresents, numPresents, maxSpeed, variation):
		self.framesBetweenPresents = framesBetweenPresents
		self.numPresents = numPresents
		self.maxSpeed = maxSpeed
		self.variation = variation
		self.presentCountdown = 0
		self.presentCounter = 0
	def reset(self):
		for present in self.presents:
			present.y = 100
			present.speed = 0
			present.setCatched(False)
			present.setMissed(False)

class Sleigh:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.width = 20
		self.height = 10

	def getLeft(self):
		return self.x

	def getRight(self):
		return self.x+self.width

	def getTop(self):
		return self.y+self.height

	def getBottom(self):
		return self.y

	def getMiddleX(self):
		return self.x+(self.width/2)

	def getMiddleY(self):
		return self.y+(self.height/2)

	def setX(self, x):
		self.x = x
# Program
# ------------------------------------------------------------------

# Global settings
global width
width = 90

# Global vars
global Slider
global sliderPos
global presents
global sleigh

# Global settings
global framesBetweenPresents
global numPresents
global maxSpeed
global variation
global presentsLeftInLevel
framesBetweenPresents = 20
numPresents = 20
maxSpeed = 2
variation = 2

# Global text
global txtLevel
global txtLives
global txtScore
global txtHighscore
global level
global lives
global score
global highscore
highscore = 0

def setLevel(value):
	global level
	level = value
	txtLevel.set_text("Level: "+str(level))

def setLives(value):
	global lives
	lives = value
	txtLives.set_text("Lives: "+str(lives))
def addLives(value):
	global lives
	global score
	lives += value
	txtLives.set_text("Lives: "+str(lives))
	if lives == 0:
		reset(score)

def setScore(value):
	global score
	score = value
	txtScore.set_text("Score: "+str(score))
def addScore(value):
	global score
	score += value
	txtScore.set_text("Score: "+str(score))

def setHighscore(value):
	global highscore
	highscore = value
	txtHighscore.set_text("Highscore: "+str(highscore))

def reset(latestScore):
	global framesBetweenPresents
	global numPresents
	global maxSpeed
	global variation

	setLives(10)
	setScore(0)
	if latestScore > highscore:
		setHighscore(latestScore)
	presents.reset()

	gotoLevel(1)
	presents.start(framesBetweenPresents, numPresents, maxSpeed, variation)

def gotoLevel(level):
	global framesBetweenPresents
	global numPresents
	global maxSpeed
	global variation
	global presentsLeftInLevel

	setLevel(level)

	framesBetweenPresents = int(30-(level/1.2))
	if framesBetweenPresents < 8:
		framesBetweenPresents = 8
	numPresents = level+9
	if numPresents > 100:
		numPresents = 100
	maxSpeed = level*0.2
	variation = level*0.15
	if variation > 3:
		variation = 3
	print(str(framesBetweenPresents)+"/"+str(numPresents)+"/"+str(maxSpeed)+"/"+str(variation))

	presentsLeftInLevel = numPresents

	presents.reset()
	presents.start(framesBetweenPresents, numPresents, maxSpeed, variation)
def gotoNextLevel():
	global level
	level += 1
	gotoLevel(level)

def onController(val):
	sliderPos = val
	controller_1.set_x(84*sliderPos)
	controller_2.set_x((84*sliderPos)+2)
	controller_3.set_x((84*sliderPos)+2)
	sleigh.setX(84*sliderPos)

def render(frame):
	global numPresents

	presents.update()
	for present in presents.getPresents():

		if present.getMiddleX() > sleigh.getLeft() and present.getMiddleX() < sleigh.getRight() and present.getBottom() < sleigh.getTop() and present.getBottom() > sleigh.getMiddleY() and not present.isCatched():
			present.setCatched(True)
			print("Catched")
			addScore(level)
			numPresents -= 1
		elif not present.isCatched() and not present.isMissed() and present.getTop() < 0:
			present.setMissed(True)
			print("Missed")
			addLives(-1)
			numPresents -= 1
	if numPresents == 0:
		gotoNextLevel()

# Setup layout
gs = gridspec.GridSpec(2, 1, height_ratios=[1, 0.05])
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_xlim(0, 100)
ax1.set_ylim(0, 100)

ax1.set_facecolor('k')

# Setup control and sleigh
sliderPos = 45
controller_1 = ptc.Rectangle((sliderPos, 7), 16, 3, facecolor=(0.8, 0.8, 0.8), edgecolor='k', linewidth='1')
ax1.add_patch(controller_1)
controller_2 = ptc.Rectangle((sliderPos+2, 3.5), 12, 3.5, color=(0.5, 0.25, 0))
ax1.add_patch(controller_2)
controller_3 = ptc.Rectangle((sliderPos+2, 0), 12, 3.5, color=(0.4, 0.2, 0))
ax1.add_patch(controller_3)

factor = Slider(ax2, 'Controller', 0, 1, valinit=0.5)
factor.on_changed(onController)

sleigh = Sleigh(sliderPos, 0)

# Setup presents
presents = PresentManager(ax1)

# Setup text
txtLevel = ax1.text(1, 90, "Level: 1", fontsize=14, color='r')
txtLives = ax1.text(1, 84, "Lives: 10", fontsize=14, color='r')
txtScore = ax1.text(1, 78, "Score: 0", fontsize=12, color='r')
txtHighscore = ax1.text(1, 70, "Highscore: 0", fontsize=10, color='r')

reset(0)

ani = animation.FuncAnimation(plt.gcf(), render, interval=40)
plt.tight_layout()
plt.show()
