import sys
import threading
import os
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from playsound import playsound
import datetime

window_length = 1000
window_height = 610

class GUI():

    def __init__(self):
        self.run()


    def run(self):
        global s, w, app
        global p
        p = Player()

        # Initialize Window
        app=QApplication(sys.argv)
        w = QWidget()

        #Window Settings
        #'image: url(WaterBG);')
        w.setGeometry(100, 100, window_length, window_height)
        w.setWindowTitle('AlchemyClickerV1.0')
        #pallete=w.palette()
        #pallete.setColor(w.backgroundRole(), Qt.red)
        #w.setPalette(pallete)
        #w.setStyleSheet("")

        playsound('sounds/click.WAV')
        setTitle()  # Add Title Block
        setWaterBtn()  # Button1: Get Water:
        setScore()  # Display Score Label:
        setProgBar()  # Progress Bar
        setbrewingStandBtn() # Brewing Stand Btn
        setNetherWart() # Add nether wart button
        updateAll()

        # Add All Building Buttons
        for Potion.Potion in potion_list:
            Potion.draw(Potion.Potion)
        for Building.Building in building_List:
            Building.draw(Building.Building)

        updateTimer()
        # Finalize window
        w.show()



        sys.exit(app.exec_())


def format_number(n):
    if n >= 1000000000:
        if (n / 1000000000 )% 1 == 0:
            n = '{:.0f} Billion'.format(n / 1000000000)
        else:
            n = '{:.2f} Billion'.format(n / 1000000000)
    elif n >= 1000000:
        if (n / 1000000) % 1 == 0:
            n = '{:.0f} Million'.format(n / 1000000)
        else:
            n = '{:.2f} Million'.format(n / 1000000)
    elif n > 1000:
        n='{:,.0f}'.format(n)

    else:
        n = '{:,.2f}'.format(n)

    return n

def updateScore():
    p.score += p.buildingCPS * p.buildings * .05
    p.getCps()
    s.setText('Potions = ' + str(format_number(p.score)) + '\nper second: ' + str(format_number(p.buildingCPS + p.CPS)))


def updateAll():
    s.setText('Potions = ' + str(format_number(p.score)) + '\nper second: ' + str(format_number(p.buildingCPS)))


def updateButtons():
    global BB
    BB = Building.Building
    for BB in building_List:
        #Update Visibility
        if p.score < BB.totalCost() or (BB.ingredient and p.waitIngredients):
            BB.button.setEnabled(False)
        else:
            BB.button.setEnabled(True)

        #Update Text
        if BB.clickPower > 0 :
            BB.button.setText(
                str(BB.name + '\nPrice: ' + str(format_number(BB.totalCost())) + '\n+' + str(format_number(p.waterPerClick)) + ' /Click'))
        else:
            BB.button.setText(str(BB.name + '\nPrice: ' + str(format_number(BB.totalCost())) + '\n +' + str(format_number(BB.cps * BB.quantity)) + ' PPS'))

    #update Nether Wart Button
    if p.score > 1000000000:
        nWartBtn.setEnabled(True)
    else:
        nWartBtn.setEnabled(False)
    #update BrewingStand button
    if p.score > 10000 and p.waitIngredients:
        brewingStandBtn.setEnabled(True)
    else:
        brewingStandBtn.setEnabled(False)

def updateTimer():
    threading.Timer(.05, updateTimer).start()
    updateButtons()
    updateScore()

#######################################################################
class Building:

    def __init__(self, name, x, y, icon, base_cost, increase_per_purchase, cps, clickPower, ingredient):
        self.x=x
        self.y=y
        self.length=200
        self.height=80
        self.name=name
        self.button= name
        self.icon=icon
        self.quantity=0
        self.base_cost=base_cost
        self.increase_per_purchase=increase_per_purchase
        self.cps=cps
        self.clickPower = clickPower
        self.ingredient = ingredient
        self.created=0

    def totalCost(self):
        return int(self.base_cost * (self.increase_per_purchase ** self.quantity))

    '''Draw Each Button '''
    def draw(self):
        global btn
        btn = QPushButton(w)
        btn.setIcon(QIcon(self.icon))
        btn.setIconSize(QSize(80, 70))
        btn.setGeometry(self.x, self.y, self.length, self.height)
        btn.clicked.connect(lambda: p.addBuilding(self, self.totalCost(), self.cps, self.clickPower))
        if p.score <= self.totalCost() or self.ingredient == True:
            btn.setEnabled(False)
        self.button = btn

    '''Buildings'''

#                   = Building(name=, x=, y= , icon=, base_cost=, increase_per_purchase= , cps=, clickPower=0 )
biggerBottles       = Building(name='Bigger Bottles', x=200, y=120, icon='WaterPot+', base_cost=100, increase_per_purchase=2.2 , cps=0, clickPower= 2, ingredient= False )
waterSourceBlock    = Building(name='Water Source', x=200, y=320, icon='waterSource', base_cost= 15, increase_per_purchase= 1.15, cps= .15, clickPower=0, ingredient= False)
cleric              = Building(name='Cleric', x=200, y=420 , icon='Cleric', base_cost=100, increase_per_purchase=1.15 , cps=1.15, clickPower=0, ingredient= False)
cauldron            = Building(name='Cauldron', x=200, y=520 , icon='cauldron', base_cost=1100, increase_per_purchase= 1.15, cps=9.2, clickPower=0, ingredient= False)
blazePowder         = Building(name='Blaze Powder', x=420, y= 320, icon='bPowder', base_cost=12000, increase_per_purchase=1.15 , cps=54, clickPower=0, ingredient= True)
redstoneDust        = Building(name='Redstone Dust', x=420, y=420, icon='rDust', base_cost=130000, increase_per_purchase=1.15, cps=300, clickPower=0,ingredient= True )
glowstoneDust       = Building(name='Glowstone Dust', x=420, y=520, icon='gDust', base_cost=1400000, increase_per_purchase=1.15, cps=2100, clickPower=0, ingredient= True )
spiderEye           = Building(name='Fermented Spider Eye', x=640, y=320, icon='sEye', base_cost=20000000, increase_per_purchase=1.15, cps=8970, clickPower=0, ingredient= True )
gunpowder           = Building(name='Gunpowder', x=640, y=420, icon='gunpowder', base_cost=330000000, increase_per_purchase=1.15, cps=357742, clickPower=0, ingredient= True )
building_List = [waterSourceBlock, cleric, biggerBottles, cauldron, blazePowder,
                 redstoneDust, glowstoneDust, spiderEye, gunpowder]


class Potion:
    def __init__(self, x, y, icon, enabled, tooltip):
        self.x=x
        self.y=y
        self.length=150
        self.height=90
        self.icon=icon
        self.enabled = enabled
        self.tooltip = tooltip

    def draw(self):
        btn=QPushButton(w)
        btn.setIcon(QIcon(self.icon))
        btn.setIconSize(QSize(self.length, self.height))
        btn.move(self.x, self.y)
        btn.setEnabled(self.enabled)
        btn.setToolTip(self.tooltip)
        btn.show()


water  = Potion(10, 10, 'WaterPot', True, 'Level 1: Shitty Ass Water Potion')
water1 = Potion(10, 110, 'WaterPot', False, 'Level 2:')
water2 = Potion(10, 210, 'qMark', False, 'Level 3:')
water3 = Potion(10, 310, 'qMark', False, 'Level 4:')
water4 = Potion(10, 410, 'qMark', False, 'Level 5:')
water5 = Potion(10, 510, 'qMark', False, 'Level 6:')

potion_list = [water, water1, water2, water3, water4, water5]




class Player():

    def __init__(self):
        # Setup date and time for clicker
        self.current = datetime.datetime.now().second
        self.score = 100000000000
        self.waterPerClick = 1
        self.globalMultipler = 1
        self.buildingCPS = 0
        self.buildings = 0
        self.waitIngredients = True
        self.wart = 90
        self.clickers = 0
        self.clicks = 0

    def addScore(self):
        self.score+=1

    def addScoreClick(self):
        self.score+=self.waterPerClick
        playsound('sounds/buy1.WAV', block=False)
        self.clicks += 1

    def getCps(self):
        if datetime.datetime.now().second != self.current:
            self.CPS= self.clicks * self.waterPerClick
            self.clicks=0
            self.current=datetime.datetime.now().second


    def addBuilding(self, building, cost, cps, clickPower):
        if self.score >= cost:
            self.buildings+=1
            self.score-=cost
            self.buildingCPS+=cps
            building.quantity += 1  #TODO fix clickers interacting withh this
            self.clickers+= 1
            if clickPower != 0:
                self.waterPerClick *= (clickPower)
            playsound('sounds/click.WAV', block=False)

    def addBuildingCPS(self, cps):
        self.buildingCPS+=cps

    def brewingStand(self):
        if self.score > 10000:
            playsound('sounds/BrewingStandSound.WAV', block=False)
            self.score -= 10000
            brewingStandBtn.setEnabled(False)
            self.waitIngredients = False


    def addNetherWart(self):
        if self.score >= 1000000000:
            playsound('sounds/levelUp.WAV', block=False)
            self.wart += 1
            self.score -= 1000000000
            pBar.setValue(self.wart)
        if self.wart >= 100:
            playsound('sounds/levelUpEpic.WAV', block=False)

#######################################################################
# BUTTON / LABEL FUNCTIONS: Mundane Potion
#######################################################################

def setScore():
    global s
    s=QLabel(w)
    s.setText('Score = ' + str(p.score) + '\nCPS: ' + str(p.buildingCPS))
    s.resize(1000, 70)
    s.setFont(QFont('Times font', 18))
    s.setAlignment(Qt.AlignHCenter)

def setTitle():
    global title
    title=QLabel("AlchemyClicker V1.0", w)
    title.resize(1000, 70)
    title.move(0, 240)
    title.setAlignment(Qt.AlignHCenter)


def setbrewingStandBtn():
    global brewingStandBtn
    brewingStandBtn=QPushButton(str('Brewing Stand' + '\nPrice: 10000' + '\nUnlocks Ingredients'), w)
    brewingStandBtn.setIcon(QIcon('BrewingStand'))
    brewingStandBtn.setIconSize(QSize(80, 70))
    brewingStandBtn.setGeometry(630, 120, 200, 80)
    brewingStandBtn.clicked.connect(lambda: p.brewingStand())
    brewingStandBtn.clicked.connect(lambda: updateScore())


def setWaterBtn():
    global waterBtn
    waterBtn=QPushButton(w)
    waterBtn.setIcon(QIcon("WaterPot"))
    waterBtn.setIconSize(QSize(160, 160))
    waterBtn.move(420, 70)
    waterBtn.clicked.connect(lambda: p.addScoreClick())  # Add 1 to score

def setNetherWart():
    global nWartBtn
    nWartBtn=QPushButton(str('Nether Wart' + '\nPrice: 1 Billion' + '\nUnlocks Next\nPotion'), w)
    nWartBtn.setIcon(QIcon('NetherWart'))
    nWartBtn.setIconSize(QSize(80, 70))
    nWartBtn.setGeometry(640, 520, 200, 80)
    nWartBtn.clicked.connect(lambda: p.addNetherWart())
    nWartBtn.setEnabled(False)


def setProgBar():
    global pBar
    pBar=QProgressBar(w)
    pBar.setOrientation(Qt.Vertical)
    pBar.setAlignment(Qt.AlignHCenter)
    pBar.setRange(0, 100)
    pBar.resize(40, 500)
    pBar.move(900, 80)
    pBar.setValue(p.wart)

    # Progress Goal
    global prog
    prog=QLabel("Goal: 100 Nether Warts", w)
    prog.resize(250, 50)
    prog.setAlignment(Qt.AlignHCenter)
    prog.move(800, 50)
