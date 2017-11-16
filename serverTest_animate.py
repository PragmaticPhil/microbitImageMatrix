from microbit import*
import radio
radio.on()
radio.config(length=50, queue=10, channel=11, power=6)

initStuff = True
pause = True
animationDirection = 1

#This will send 10 frames - an animation - to Node0

def test_Send_n0():
    radio.send("pX100000000000000:00000:00900:00000:00000")
    sleep(25)
    radio.send("pX100000100000000:00900:09090:00900:00000")
    sleep(25)
    radio.send("pX100000200000900:00900:99099:00900:00900")
    sleep(25)
    radio.send("pX100000300000900:90909:99099:90909:00900")
    sleep(25)
    radio.send("pX100000400009990:90909:99099:90909:09990")
    sleep(25)
    radio.send("pX100000500099999:90009:90009:90009:99999")
    sleep(25)
    radio.send("pX100000600099099:90009:00000:90009:99099")
    sleep(25)
    radio.send("pX100000700090009:00000:00000:00000:90009")
    sleep(25)
    radio.send("pX100000800090009:09090:00000:09090:90009")
    sleep(25)
    radio.send("pX100000900000000:09090:00000:09090:00000")
    sleep(25)


def test_Send_n1():
	radio.send("pX100000000090000:09000:00000:00000:00000")
	sleep(25)
	radio.send("pX100000100099000:90000:00000:00000:00000")
	sleep(25)
	radio.send("pX100000200099900:90000:90000:00000:00000")
	sleep(25)
	radio.send("pX100000300099999:90000:90000:90000:00000")
	sleep(25)
	radio.send("pX100000400099999:90000:90000:90000:90000")
	sleep(25)
	radio.send("pX100000500090000:09999:09000:09000:09000")
	sleep(25)
	radio.send("pX100000600090000:09000:00999:00900:00900")
	sleep(25)
	radio.send("pX100000700090000:09000:00900:00099:00090")
	sleep(25)
	radio.send("pX100000800090000:09000:00900:00090:00009")
	sleep(25)
	radio.send("pX100000900090000:09000:00900:00000:00000")
	sleep(25)    

def test_Send_n2():
	radio.send("pX100000000000900:00900:99999:00900:00900")
	sleep(25)
	radio.send("pX100000100009000:09000:99999:00090:00090")
	sleep(25)
	radio.send("pX100000200090000:90000:99999:00009:00009")
	sleep(25)
	radio.send("pX100000300009000:09000:99999:00090:00090")
	sleep(25)
	radio.send("pX100000400000900:00900:99999:00900:00900")
	sleep(25)
	radio.send("pX100000500000900:99900:00900:00999:00900")
	sleep(25)
	radio.send("pX100000600099900:00900:00900:00900:00999")
	sleep(25)
	radio.send("pX100000700000900:99900:00900:00999:00900")
	sleep(25)
	radio.send("pX100000800000900:00900:99999:00900:00900")
	sleep(25)
	radio.send("pX100000900000000:00900:09990:00900:00000")
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
    radio.send("pX0600205999")      # _2r_5c


while True:
    display.show(".")
    
    if(button_a.was_pressed()):  
        if(initStuff):
            display.show("1")
            setMatrixDims()
            sleep(250)
            test_Send_n1()
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
            
