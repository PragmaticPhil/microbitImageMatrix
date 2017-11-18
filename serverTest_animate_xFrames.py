from microbit import*
import radio
radio.on()
radio.config(length=50, queue=10, channel=11, power=6)

initStuff = True
pause = True
animationDirection = 1

#This will send 10 frames - an animation - to Node0

def test_Send_n0():
	radio.send("pX100000000099999:00000:00000:00000:00000")
	sleep(25)
	radio.send("pX100000100000000:99999:00000:00000:00000")
	sleep(25)
	radio.send("pX100000200000000:00000:99999:00000:00000")
	sleep(25)
	radio.send("pX100000300000000:00000:00000:99999:00000")
	sleep(25)
	radio.send("pX100000400000000:00000:00000:00000:99999")
	sleep(25)
	

def test_Send_n1():
	radio.send("pX100000000199999:00000:00000:00000:00000")
	sleep(25)
	radio.send("pX100000100100000:99999:00000:00000:00000")
	sleep(25)
	radio.send("pX100000200100000:00000:99999:00000:00000")
	sleep(25)
	radio.send("pX100000300100000:00000:00000:99999:00000")
	sleep(25)
	radio.send("pX100000400100000:00000:00000:00000:99999")
	sleep(25)
	

def test_Send_n2():
	radio.send("pX100000000299999:00000:00000:00000:00000")
	sleep(25)
	radio.send("pX100000100200000:99999:00000:00000:00000")
	sleep(25)
	#radio.send("pX100000200200000:00000:99999:00000:00000")
	#sleep(25)
	radio.send("pX100000300200000:00000:00000:99999:00000")
	sleep(25)
	radio.send("pX100000400200000:00000:00000:00000:99999")
	sleep(25)
    

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

def setMatrixDims():
    radio.send("pX0600205")      # _2r_5c

def setNumberOfFrames():
    radio.send("pX0610005")         # 5 FRAMES

def sendBufferSizeCheck():
    radio.send("pX090")         # 5 FRAMES


while True:
    display.show(".")
    
    if(button_a.was_pressed()):  
        display.show("i")
        if(initStuff):
            display.show("1")
            setMatrixDims()
            sleep(250)
            test_Send_n0()
            sleep(250)
            test_Send_n1()
            sleep(250)
            test_Send_n2()
            sleep(250)            
            setNumberOfFrames()
            sleep(250)
            sendBufferSizeCheck()
            initStuff = False
        else:
            if(pause):
                display.show("P")
                unPause()
                pause = False
                sleep(250)
            else:
                display.show("T")
                doPause()
                pause = True
                sleep(250)
                

    if(accelerometer.was_gesture('left')):
        display.show("L")
        scrollLeft()
        sleep(500)
        unPause()


    if(accelerometer.was_gesture('right')): 
        display.show("R") 
        scrollRight()
        sleep(500)


        
    if(button_b.was_pressed()):
        if(animationDirection == 1):
            animateLeft()
            animationDirection = -1
            display.show(">")
            sleep(250)
        else:
            animateRight()
            animationDirection = 1
            display.show("<")
            sleep(250)
            
