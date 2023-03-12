'''
class Player():

    def __init__(self):
        self.score=490
        self.wart=0
        self.waterPerClick=1
        self.waterSource=0
        self.WSprice=10
        self.biggerBottlesPrice=20
        self.globalMultipler=1
        self.cleric=0
        self.clericPrice=500
        self.buildingCPS=0
        self.buildings = 0


    def addScore(self):
        self.score+=1

    def addScoreClick(self):
        self.score+=self.waterPerClick

    def addBuilding(self, cost, cps):
        print(cost, self.buildings, self.buildingCPS)
        if self.score >= cost:
            self.buildings += 1
            self.score -= cost
            self.buildingCPS += cps


    def addBuildingCPS(self, cps):
        self.buildingCPS += cps


'''