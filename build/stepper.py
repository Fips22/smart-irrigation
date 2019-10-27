from machine import Timer
from machine import Pin

# only test for uln2003
class Stepper:

    # nur für fullstep, noch für halfstep definieren und in logik einbinden
    FULL_ROTATION = int(4075.7728395061727/2) # http://www.jangeox.be/2013/10/stepper-motor-28byj-48_25.html


    HALF_STEP = [
        [0, 0, 0, 1],
        [0, 0, 1, 1],
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 1], 
    ]

    FULL_STEP = [
        [1, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 0, 1]
    ]
    def __init__(self, pin1, pin2, pin3, pin4, maxSpeed = 100 ,maxSteps = 0 , mode = 'FULL_STEP'):

        #steps/s
        self.stepsPS = int(1000/maxSpeed)

    	if mode=='FULL_STEP':
        	self.mode = self.FULL_STEP
        else:
        	self.mode = self.HALF_STEP

        self.currStepBitPos = 0
        self.stepsToRun = 0
        self.pos=0
        self.maxSteps = maxSteps
        self.pin1 = Pin(pin1,Pin.OUT)
        self.pin2 = Pin(pin2,Pin.OUT)
        self.pin3 = Pin(pin3,Pin.OUT)
        self.pin4 = Pin(pin4,Pin.OUT)
        self.timer = Timer(-2)
        self.callback = None
        
        # Initialize all to 0
        self.reset()

    def setMotionEndCB(self,cb):

        self.callback = cb

    def step(self,t):

        direction = -1
        if self.stepsToRun > 0:
            direction = 1
            self.pos +=1

        if self.stepsToRun < 0:
            self.pos -=1

        self.stepsToRun = self.stepsToRun - direction #zähle einen richtung 0

        self.currStepBitPos = self.currStepBitPos+direction   #ändere position im steparray um eine stelle 

        if self.currStepBitPos > len(self.mode)-1:
            self.currStepBitPos = 0

        if self.currStepBitPos < 0:
            self.currStepBitPos = len(self.mode)-1

        bit = self.mode[self.currStepBitPos]

        self.pin1(bit[0])
        self.pin2(bit[1])
        self.pin3(bit[2])
        self.pin4(bit[3])
                
        if self.stepsToRun < 0 or self.stepsToRun > 0:

            self.timer.init(period = self.stepsPS, mode=Timer.ONE_SHOT, callback=self.step)
        else:
            self.reset()

            if self.callback is not None:
                self.callback()

    def angle(self, r, direction=1,speed = None):
    	self.run(int(self.FULL_ROTATION * r / 360), direction , speed)

    def stop(self):
        self.stepsToRun = 0

    def reset(self):
        # Reset to 0, no holding, these are geared, you can't move them
        self.pin1(0) 
        self.pin2(0) 
        self.pin3(0) 
        self.pin4(0)

    def resetPos(self):
        self.pos = 0

    def getPos(self):
        return self.pos

    def run(self , steps , dire = 1, speed = None):

        if self.maxSteps > 0 and self.pos+steps*dire > self.maxSteps:   #wenn maximal Anzahl an schritten überschritten werden soll brich ab
            return False

        if speed is not None:
            self.stepsPS = int(1000/speed)

        self.stepsToRun =  steps * dire
        self.step(None)

        return True
