from microbit import*
import radio
radio.on()
radio.config(length=50, queue=10, channel=11, power=6)

global currentDeviceAction
currentDeviceAction = 0

global isPaused
isPaused = False

global updateSpeed
updateSpeed = 250

# SETTING UP PINS FOR INPUT:
# 1 = momentary buttons:
button_n = pin13                #currentDeviceAction = 1
button_e = pin14                #currentDeviceAction = 2
button_s = pin15                #currentDeviceAction = 3
button_w = pin16                #currentDeviceAction = 4


# 2 = buzzer:
buzzer_Output = pin0
global playBuzzer
playBuzzer = False

# 3 = potentometer (used to select element of house being changed):
deviceSelector = pin1
global deviceSelected
deviceSelected = 0

# 4 = Toggle switch (animation / scroll):
global toggleAnimationType
toggleAnimationType = True
onoff_Local = pin12



def setCurrentButtonPress():    # records which (if any) of the momentary buttons are currently being pressed
    global onoff_local
    global playBuzzer
    global currentDeviceAction
    global toggleAnimationType
    
    toggleAnimationType = (onoff_Local.read_digital() == 0)
    #print("Animation toggel = " + str(toggleAnimationType))
    
    if(button_n.read_digital() == 1):
        currentDeviceAction = 1
        print("Button North pressed")
        playBuzzer = True
        return
    if(button_e.read_digital() == 1):
        currentDeviceAction = 2
        print("Button East pressed")
        playBuzzer = True
        return
    if(button_s.read_digital() == 1):
        currentDeviceAction = 3
        print("Button South pressed")
        playBuzzer = True
        return
    if(button_w.read_digital() == 1):
        currentDeviceAction = 4
        print("Button West pressed")
        playBuzzer = True
        return



def playTheBuzzer(buzzerTone):
    global playBuzzer    
    buzzer_Output.write_analog(buzzerTone)
    sleep(50)
    print("Buzzer buzzed")
    buzzer_Output.write_analog(0)
    playBuzzer = False
    

def setSpeedLevel():
    global updateSpeed
    potBufVal = deviceSelector.read_analog()
    potNewVal = int( (potBufVal ) / 2)
    
    if( (potNewVal > (updateSpeed + 25)) or (potNewVal < (updateSpeed - 25)) ):
        updateSpeed = potNewVal
        sendNewSpeed (550-updateSpeed)

def sendNewSpeed(newSpeed):
    if(newSpeed < 10):      newSpeed = 10
    if(newSpeed < 100):     
        print("Sending: pX06600" + str(newSpeed))
        radio.send("pX06600" + str(newSpeed))
        return
    if(newSpeed < 1000):
        print("Sending: pX0660" + str(newSpeed))    
        radio.send("pX0660" + str(newSpeed))    


def issueCurrentDeviceCommand():     # 0 = OFF, 1 = ON
    global currentDeviceAction
    global deviceSelected
    global isPaused

    print("Issuing device command: " + str(currentDeviceAction))

    if(currentDeviceAction == 3):                                               # SOUTH
        isPaused = not(isPaused)
        if(isPaused):               radio.send("pX080")
        if(not(isPaused)):          radio.send("pX081")

    if(toggleAnimationType):            # TRUE means type is ANIMATION
        if(currentDeviceAction == 1):   radio.send("pX082000")                      # NORTH.  All synch to frame 0
        if(currentDeviceAction == 2):   radio.send("pX068")                         # EAST 
        if(currentDeviceAction == 4):   radio.send("pX067")                         # WEST
    else:                               # FALSE means type is SCROLL
        if(currentDeviceAction == 1):   radio.send("pX083000")                      # NORTH.  All synch to frame 0 + nodeID
        if(currentDeviceAction == 2):   radio.send("pX063")                         # EAST 
        if(currentDeviceAction == 4):   radio.send("pX062")                         # WEST     

    currentDeviceAction = 0     # ensure we don't persist the command

def setInputParameters():       # review board and set relevant params:
    setSpeedLevel()
    setCurrentButtonPress()





while True:
    sleep(100)
    setInputParameters()    # scans the board to see what is off / on and sets params accordingly
    
    if(playBuzzer):
        playTheBuzzer(100)
        #print(str(currentDeviceAction))    

    #print("In main: " + str(currentDeviceAction))
    
    if(currentDeviceAction > 0):     # >0 means a valid command has been issued:
        issueCurrentDeviceCommand()
            
    
        
