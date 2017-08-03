from microbit import*
import radio
radio.on()
radio.config(length=64, queue=8, channel=11, power=6)

frameCount = 0

while True:
    
    if(frameCount == 0): frameCount = 0
    
    if(button_a.is_pressed()):  
        radio.send("pXa000990001!99999:90009:90009:90009:90009")
        sleep(20)
        radio.send("pXa001990001!00900:00900:00900:00900:00900")
        sleep(20)
        radio.send("pXa002990001!00999:00009:00099:00990:00999")
        sleep(20)
        radio.send("pXa003990001!09999:00009:00999:00009:09999")
        sleep(20)

        display.show("a")
        radio.send("pXb999020001")
        display.show("A")
     
    #if(button_a.is_pressed()):  
    #    radio.send("pXb99902000" + str(frameCount))
    #    frameCount += 1
    #    display.show("a")
        
    if(button_b.is_pressed()):  
        radio.send("pXb999020000")
        display.show("0")
        sleep(500)
        radio.send("pXb999020001")
        display.show("1")
        sleep(500)
        radio.send("pXb999020002")
        display.show("2")
        sleep(500)
        radio.send("pXb999020003")
        display.show("3")
        sleep(500)
        radio.send("pXb999020004")
        display.show("4")
        sleep(500)
        radio.send("pXb999020005")
        display.show("5")
        sleep(500)
        radio.send("pXb999020006")
        display.show("6")
        sleep(500)
        radio.send("pXb999020007")
        display.show("7")
        sleep(500)
        radio.send("pXb999020008")
        display.show("8")
        sleep(500)
        radio.send("pXb999020009")
        display.show("9")
        sleep(500)
        display.show("X")