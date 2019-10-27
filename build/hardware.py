from machine import ADC
from machine import Pin
import ujson
from stepper import Stepper



#---------------------------------------------------------



class analogmultiplexcontrol:

    # ============================================================================
    # ===( Constants )============================================================
    # ============================================================================

    # ============================================================================
    # ===( Class globals  )=======================================================
    # ============================================================================

    # ============================================================================
    # ===( Utils  )===============================================================
    # ============================================================================

    # ============================================================================
    # ===( Constructor )==========================================================
    # ============================================================================

    def __init__(self, configFile = "hardware.cfg",config = None):

        #---------------------------------------------------------

        if config == None:

            f = open('hardware.cfg')

            hardconfobj = ujson.loads(f.read())

            config = hardconfobj["input"]

            f.close()



        #init all adc pins
        self.adc = []
        x = 0

        for pin in config["analogInputs"]:

            self.adc[x]=ADC(Pin(pin)) # create ADC object on ADC pin
            self.adc[x].atten(ADC.ATTN_11DB)# set 11dB input attenuation 
            self.adc[x].width(ADC.WIDTH_9BIT)

            x +=1


        self.mplex = []
        x = 0

        for pin in config["multiplexerPins"]:
            self.mplex[x]=Pin(pin, Pin.OUT) 
            self.mplex[x].off()
            x +=1

    # ============================================================================
    # ===( Functions )============================================================
    # ============================================================================

    def readInput(self,number):
    		
    	mod = number % 5 # =index of analogpin

    	multiplexarray = '{0:04b}'.format((number - mod)/5)#  get the binary array of the 
    	i=0

        for x in multiplexarray:
        	
        	self.mplex[i].value(int(x))
        	
        	i +=1

    	return self.adc[mod].read()



class valvecontrol:

    # ============================================================================
    # ===( Constants )============================================================
    # ============================================================================
    _m5_steigung = 0.8


    # ============================================================================
    # ===( Class globals  )=======================================================
    # ============================================================================

    
 
    # ============================================================================
    # ===( Utils  )===============================================================
    # ============================================================================

    # ============================================================================
    # ===( Constructor )==========================================================
    # ============================================================================

    def __init__(self, configFile = "hardware.cfg",config = None):

        if config == None:

            f = open('hardware.cfg')

            hardconfobj = ujson.loads(f.read())

            self.config = hardconfobj["valve"]

            f.close()

        else:
            self.config = config

        #self.config["homeSencePin"]
        #self.config["homePosToValve"] in mm
        #self.config["valveToValve"] in mm
        #self.config["valveAmmount"]
        #self.config["maxSteps"]

                                    # mm von ventil zu ventil * schritte pro umdrehung / gewindesteigung
        self.stepsValveToValve = int(self.config["valveToValve"] * ((4075.7728395061727/2)/self._m5_steigung) )
        print(self.stepsValveToValve)

        self.stepshomePosToValve = int(self.config["homePosToValve"] * ((4075.7728395061727/2)/self._m5_steigung) )

        self.homingIsrunning = False
        self.valveReachedCB = None
        self.homingCB = None


        self.homepin = Pin(self.config["homeSencePin"], Pin.IN)
        

        pin = self.config["stepperPins"]

        self.valveStepper = Stepper(pin[0],pin[1],pin[2],pin[3],self.config["steps-s"],self.config["maxSteps"])

    def setValveReachedCB(self,cb):
        self.valveReachedCB = cb 


    def setHomeFinishedCB(self,cb):
        self.homingCB = cb

    def _internalHomingCallback(self,e):

        if self.homingIsrunning == True:
            self.homingIsrunning = False
            self.valveStepper.stop()
            self.valveStepper.resetPos()
            print("internal call")

            if self.homingCB is not None:
                self.homingCB()


    def homing(self,speed = None):
        #triggerflanke noch bestimmen!!!
        self.homingIsrunning = True

        # 
        #print(self.homepin.value())
        #todo: test if homepin is triggered
        #if true go in postitive direction and home after 
        #if false home 


        self.homepin.irq(trigger=Pin.IRQ_RISING , handler=self._internalHomingCallback)
        self.valveStepper.run(-1000000,1,speed)


    def openValve(self,valve): 

        if valve > self.config["valveAmmount"]:
            return False
        
        stepsToRun = self.stepshomePosToValve + ((valve-1) * self.stepsValveToValve) - self.valveStepper.getPos()
        print("stepsToRun")
        print(stepsToRun)

        self.valveStepper.setMotionEndCB(self.valveReachedCB)
        self.valveStepper.run(stepsToRun)

    def run(self , steps , dire = 1, speed = None):
        self.valveStepper.run(steps,dire,speed)



    def closeAll(self):
        self.valveStepper.setMotionEndCB(self.valveReachedCB)
        self.valveStepper.run(self.config["valveToValve"]/2) 

    def readHomePin(self):

        print("pin")
        print(self.homepin)
        print(self.homepin.value())

    def closeInHome(self):
        
        stepsToRun = -(self.stepshomePosToValve + self.valveStepper.getPos())
        print("stepsToRun")
        print(stepsToRun)
        






class pumpcontrol:

	# ============================================================================
    # ===( Constants )============================================================
    # ============================================================================
    


    # ============================================================================
    # ===( Class globals  )=======================================================
    # ============================================================================

    
 
    # ============================================================================
    # ===( Utils  )===============================================================
    # ============================================================================

    # ============================================================================
    # ===( Constructor )==========================================================
    # ============================================================================

    def __init__(self, configFile = "hardware.cfg",config = None):

        print("test")






  


#adc[].read()                  # read value, 0-511 across voltage range 0.0v - 3.6v
 

#---hardware.cfg--- 
#inhalt:
#    config der analogeingänge: 
#		multiplexer signalpins 0-3
#		genutze analogeingänge 0-4
"""
ADC1_CH3 >>> GPIO39
ADC1_CH6 >>> GPIO34
ADC1_CH7 >>> GPIO35
ADC1_CH4 >>> GPIO32
ADC1_CH5 >>> GPIO33
"""

"""


"""
#		(16 multiplexereingänge x 5= 80 eingänge)
#		------------------------
#       gemessener Spannungsbereich
#       auflösung
#       anzahl an verfügbaren eingängen (duch multiplexer oder i2c auch viel mehr)
#    ventile:
#       anzahl ventile
#       stepps von homepos zu 1.ventil
#       stepps von ventil zu ventil
#       maximale stepps bis ende
#       max geschwindigkeit
#       max beschleunigung
#    pumpe:
#        stepps pro ml oder t/ml
#        betriebsmodus(stepper oder dc motor)
