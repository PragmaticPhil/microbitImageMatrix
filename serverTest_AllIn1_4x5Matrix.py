from microbit import*
import radio
radio.on()
radio.config(length=50, queue=10, channel=11, power=6)

toggleImageServed = True
togglePauseOn = True
toggleAnimationTypeScroll = True

#This will send 5 frames - an animation - to ALL nodes:

def test_Send_ALL_5Frames():
	radio.send("pX140000000099999:00000:00000:00000:00000")
	sleep(25)
	radio.send("pX140000100000000:99999:00000:00000:00000")
	sleep(25)
	radio.send("pX140000200000000:00000:99999:00000:00000")
	sleep(25)
	radio.send("pX140000300000000:00000:00000:99999:00000")
	sleep(25)
	radio.send("pX140000400000000:00000:00000:00000:99999")
	sleep(25)


def test_Send_Row0_10Frames():
	radio.send("pX120000000000900:09990:90909:90909:90909")
	sleep(25)
	radio.send("pX120000100000900:00000:09900:00900:00900")
	sleep(25)
	radio.send("pX120000200000000:09990:90000:90000:09990")
	sleep(25)
	radio.send("pX120000300000000:09999:99000:09000:09000")
	sleep(25)
	radio.send("pX120000400000000:00990:09009:09009:00990")
	sleep(25)
	radio.send("pX120000500009900:09900:00000:09900:09900")
	sleep(25)
	radio.send("pX120000600090000:90000:99990:90090:99990")
	sleep(25)
	radio.send("pX120000700000900:00000:09900:00900:00900")
	sleep(25)
	radio.send("pX120000800009000:99990:09000:09000:09990")
	sleep(25)
	radio.send("pX120000900000900:00900:00900:00000:00900")
	sleep(25)


def setMatrixDims():
    radio.send("pX0600405")      # _2r_5c

def setNumberOfFrames5():
    radio.send("pX0610005")         # 5 FRAMES

def setNumberOfFrames10():
    radio.send("pX0610010")         # 10 FRAMES

def sendBufferSizeCheck():
    radio.send("pX090")         # 5 FRAMES

def sendReset():
    radio.send("pX099")

def doPause():
    radio.send("pX080")

def unPause():
    radio.send("pX081")

def scrollLeft():
    radio.send("pX062")
    
def scrollRight():
    radio.send("pX063")

def animateLeft():
    radio.send("pX067")    

def animateRight():
    radio.send("pX068")


while True:
    display.show(".")
    
    if(button_a.was_pressed()):
        if(toggleImageServed):
            display.show("a")
            setMatrixDims()
            sleep(250)
            setNumberOfFrames5()
            sleep(250)
            test_Send_ALL_5Frames()
            sleep(250)
            sendBufferSizeCheck()
            sleep(250)
            toggleImageServed = False
        else:
            display.show("A")
            setMatrixDims()
            sleep(250)
            setNumberOfFrames10()
            sleep(250)
            test_Send_Row0_10Frames()
            sleep(250)
            sendBufferSizeCheck()
            sleep(250)
            toggleImageServed = True


    if(accelerometer.was_gesture('shake')):
        if(togglePauseOn):
            display.show("P")
            doPause()
            sleep(500)
            togglePauseOn = False
        else:
            display.show("p")
            unPause()
            sleep(500)
            togglePauseOn = True
            

    if(accelerometer.was_gesture('left')):
        if(toggleAnimationTypeScroll):
            display.show("s")
            scrollLeft()
            sleep(500)
        else:
            display.show("n")
            animateLeft()
            sleep(500)
            

    if(accelerometer.was_gesture('right')): 
        if(toggleAnimationTypeScroll):
            display.show("S")
            scrollRight()
            sleep(500)
        else:
            display.show("N")
            animateRight()
            sleep(500)


    if(button_b.was_pressed()):
        if(toggleAnimationTypeScroll):
            display.show("b")
            toggleAnimationTypeScroll = False
            sleep(500)
        else:
            display.show("B")
            toggleAnimationTypeScroll = True
            sleep(500)
            
