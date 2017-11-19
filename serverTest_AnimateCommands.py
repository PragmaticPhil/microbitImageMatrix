from microbit import*
import radio
radio.on()
radio.config(length=50, queue=10, channel=11, power=6)

pause = True
animationCommandCounter = 0

animationDirection = 1
animationType = 0


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
                
        
    if(button_b.was_pressed()):
        if(animationCommandCounter == 0):
            animateLeft()
            display.show("0")
            sleep(250)
        if(animationCommandCounter == 1):
            animateRight()
            display.show("1")
            sleep(250)
        if(animationCommandCounter == 2):
            scrollLeft()
            display.show("2")
            sleep(250)
        if(animationCommandCounter == 3):
            scrollRight()
            display.show("3")
            sleep(250)
        animationCommandCounter = animationCommandCounter + 1
        if(animationCommandCounter == 4):
            animationCommandCounter = 0
