from robot.megapi import *

right = 1
left = 2

def back(level):
    level
    #print("Encoder motor speed Value:%f" %level)

def cmtotick(target):
    #fulltick 360
    #r 3.25
    tick = ( target*360 ) // ( 2*3.14*3.25 )
    return int(tick)

def onForwardFinish(tick):
    bot.encoderMotorMover(right, 100, tick * -1)
    bot.encoderMotorMover(left, 100, tick )

def onRightFinish(tick):
    bot.encoderMotorMover(right,100, 0 * -1 )
    bot.encoderMotorMover(left, 100, tick )
    
def onLeftFinish(tick):
    bot.encoderMotorMover(right, 100, tick * -1 )
    bot.encoderMotorMover(left, 100, 0 )
    
def onBackwardFinish(tick):
    bot.encoderMotorMover(right, 100, tick )
    bot.encoderMotorMover(left, 100, tick * -1 )
    
def onExecuteDir(dir,tickR,tickL):
    if dir == "forward" :
        onForwardFinish(tickR)
    elif dir == "backward" :
        onBackwardFinish(tickL)
    elif dir == "right" :
        onForwardFinish(tickL)
    elif dir == "left" :
       onBackwardFinish(tickR)

def EncoderGroup():
    bot.encoderMotorPosition(right,back)
    bot.encoderMotorPosition(left,back)
    sleep(0.1)
    return bot.getKeeper()

if __name__ == '__main__':
    bot = MegaPi()
    bot.start("/dev/ttyUSB0")
    #bot.start("/dev/rfcomm0")

    commandDir=["forward","forward","backward","forward","forward","backward"]
    commandDist=[[40,40],[40,40],[40,40],[40,40],[40,40],[40,40]] #cm

    #commandDir=["forward","right","left","forward","backward"]
    #commandDist=[[40,40],[0,20],[20,0],[40,40],[40,40]] #cm
    
    bot.encoderMotorSetCurPosZero(right)
    bot.encoderMotorSetCurPosZero(left)
    sleep(0.5)
    
    bot.encoderMotorRun(right ,0)#right
    bot.encoderMotorRun(left ,0)#left
    
    sleep(0.1)
   
    i = 0
    targetTickRight = cmtotick(commandDist[i][0])
    targetTickLeft = cmtotick(commandDist[i][1])
    #print(targetTick)
    onExecuteDir(commandDir[i],targetTickRight,targetTickLeft)      
    
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
            if  ( abs(deltaTickRight)-20 ) < abs(targetTickRight) < ( abs(deltaTickRight)+20 ) and ( abs(deltaTickLeft)-20 ) < abs(targetTickLeft) < ( abs(deltaTickLeft)+20 ):
                 if not command:
                    print("change")
                    i+=1
                    if i>=len(commandDir):
                        break
                    print("i"+str(i))
                    targetTickRight = cmtotick(commandDist[i][0])
                    targetTickLeft = cmtotick(commandDist[i][1])
                    onExecuteDir(commandDir[i],targetTickRight,targetTickLeft)
                    lastTickRight = encRight 
                    lastTickLeft = encLeft 
                    command = True
                    sleep(0.5)
            elif command :
                command = False
            
        sleep(0.1)
        
        continue
    
        
