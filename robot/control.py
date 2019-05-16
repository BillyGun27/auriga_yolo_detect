right = 1
left = 2

#turn 28 cm
class Command:
    def __init__(self, bot ,direct, dist):
        self.bot = bot
        self.direct = direct
        self.dist = dist
        #fulltick 360
        #r 3.25
        self.tick = int( ( self.dist*360 ) // ( 2*3.14*3.25 ) )
        if self.direct == "forward" :
            self.tickR = self.tick * -1
            self.tickL = self.tick 
        elif self.direct == "backward" :
            self.tickR = self.tick 
            self.tickL = self.tick * -1
        elif self.direct == "right" :
            self.tickR = 0 
            self.tickL = self.tick * 1
        elif self.direct == "left" :
            self.tickR = self.tick * -1
            self.tickL = 0
        elif self.direct == "rightb" :
            self.tickR = 0 
            self.tickL = self.tick * -1
        elif self.direct == "leftb" :
            self.tickR = self.tick * 1
            self.tickL = 0

    def toFinish(self):
        print(self.tickR)
        self.bot.encoderMotorMover( right, 100, self.tickR)
        self.bot.encoderMotorMover( left, 100, self.tickL)
    
    def getDirect(self):
        return self.direct 
    
    def targetTickRight(self):
        return self.tickR 

    def targetTickLeft(self):
        return self.tickL