from microbit import*
import radio
radio.on()
radio.config(length=50, queue=10, channel=11, power=6)

#This will send 5 frames - an animation - to ALL nodes:

def test_Send_ALL_A():
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


def test_Send_ALL_B():
	radio.send("pX100000000099900:90090:99900:90000:90000")
	sleep(25)
	radio.send("pX100000100090000:90000:99990:90090:90090")
	sleep(25)
	radio.send("pX100000200000900:00000:00900:00900:00900")
	sleep(25)
	radio.send("pX100000300009000:09000:09000:09000:09990")
	sleep(25)
	radio.send("pX100000400009990:90009:90009:90009:09990")
	sleep(25)


def setMatrixDims():
    radio.send("pX0600405")      # _2r_5c

def setNumberOfFrames():
    radio.send("pX0610005")         # 5 FRAMES

def sendBufferSizeCheck():
    radio.send("pX090")         # 5 FRAMES

def sendReset():
    radio.send("pX099")

while True:
    display.show(".")
    
    if(button_a.was_pressed()):
        display.show("a")
        setMatrixDims()
        sleep(250)
        test_Send_ALL_A()
        sleep(250)
        setNumberOfFrames()
        sleep(250)
        sendBufferSizeCheck()
        sleep(250)

        
    if(button_b.was_pressed()):
        display.show("b")
        setMatrixDims()
        sleep(250)
        test_Send_ALL_B()
        sleep(250)
        setNumberOfFrames()
        sleep(250)
        sendBufferSizeCheck()
        sleep(250)