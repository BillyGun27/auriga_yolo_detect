from robot.megapi import *

right = 1
left = 2

#turn 28 cm
class Command:
    def __init__(self, direct, dist):
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
        bot.encoderMotorMover( right, 100, self.tickR)
        bot.encoderMotorMover( left, 100, self.tickL)
    
    def getDirect(self):
        return self.direct
    
    def targetTickRight(self):
        return self.tickR 

    def targetTickLeft(self):
        return self.tickL

def back(level):
    level
    #print("Encoder motor speed Value:%f" %level)
    

def EncoderGroup():
    bot.encoderMotorPosition(right,back)
    bot.encoderMotorPosition(left,back)
    sleep(0.1)
    return bot.getKeeper()

if __name__ == '__main__':
    bot = MegaPi()
    bot.start("/dev/ttyUSB0")
    #bot.start("/dev/rfcomm0")

    bot.encoderMotorSetCurPosZero(right)
    bot.encoderMotorSetCurPosZero(left)
    sleep(0.5)
    
    bot.encoderMotorRun(right ,0)#right
    bot.encoderMotorRun(left ,0)#left
    sleep(0.1)
    
    commandKey=[]
    commandKey.append(Command("forward",80))
    #commandKey.append(Command("backward",40))
    #commandKey.append(Command("right",28))
    #commandKey.append(Command("forward",40))
    #commandKey.append(Command("left",28))
   
    i = 0
    commandKey[i].toFinish()  
    sleep(1.5)
    
    lastTickRight = 0
    lastTickLeft = 0
    command = False
    while True:
        encodergroup =  EncoderGroup()
        print(encodergroup )
        #print(encoderkey.keys())
        
        ###wait encoder value
        if( len(encodergroup.keys()) == 2 ):
            #print(encodergroup)
            
            encRight =  encodergroup[ bot.getextId(right) ]
            encLeft = encodergroup[ bot.getextId(left) ]
        
            print("right" + str(encRight))
            print("left" + str(encLeft))
            
            deltaTickRight = encRight - lastTickRight
            deltaTickLeft = encLeft - lastTickLeft
            print("Right: Delta>{} Cur>{} Last>{}".format( deltaTickRight, encRight ,lastTickRight ))
            print("Left: Delta>{} Cur>{} Last>{}".format( deltaTickLeft, encLeft ,lastTickLeft ))
            #print("Target:{}".format(targetTick) )
             
            #Position Reached
            if  ( abs(deltaTickRight)-20 ) < abs( commandKey[i].targetTickRight() ) < ( abs(deltaTickRight)+20 ) and ( abs(deltaTickLeft)-20 ) < abs( commandKey[i].targetTickLeft() ) < ( abs(deltaTickLeft)+20 ):
                 if not command:
                    print("change")
                    i+=1
                    if i>=len(commandKey):
                        break
                    #print("i"+str(i))
                    commandKey[i].toFinish()
                    lastTickRight = encRight 
                    lastTickLeft = encLeft 
                    command = True
                    sleep(0.5)
            elif command :
                command = False
            
        sleep(0.1)
        
        continue
    
        
