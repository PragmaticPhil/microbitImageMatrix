from microbit import*
import radio
radio.on()
radio.config(length=50, queue=11, channel=11, power=6)

nodeID = 0

global totalRows
global totalCols
totalRows = 1
totalCols = nodeID + 1

global currentFrame
global pauseShowFrame
global frameSpeed
currentFrame = 0
pauseShowFrame = True
frameSpeed = 250

global animationDirection
global animationType
global scrollIndex
animationDirection = 0
animationType = 0               #   0 = Animate by Frame; 1 = Animate by scrolling
scrollIndex = 0

global imageDataStore
global totalFrames
imageDataStore = [(""),(""),(""),(""),(""),(""),(""),(""),(""),(""),]
totalFrames = 10


def getServerMessage():
    try:        return str(radio.receive())
    except:     return "X"


def processServerMessage(rawMsg):
    if(len(rawMsg) < 5):                return
    if(not(rawMsg[0 : 2] == "pX")):     return
    if(rawMsg[2 : 3] == "0"):                   processServerInstruction(rawMsg)
    else:                               
        if(isRelevantImageMessage(rawMsg)):     processImageMessage(rawMsg)


def isRelevantImageMessage(rawMsg):
#    try:
    if(not(rawMsg[2 : 3] == "1")):                                      return False
    if(rawMsg[3 : 4] == "4"):                                           return True
    if((rawMsg[3 : 5] == "00") and (int(rawMsg[9 : 12]) == nodeID)):    return True
    if((rawMsg[3 : 4] == "2") and (int(rawMsg[9 : 12]) == getRowRef())):     return True
    print("!")
    return False
#    except:


def processImageMessage(rawMsg):
    global imageDataStore
    serverMsgStr = rawMsg[3 : 5]
    frameRef = int(rawMsg[5 : 9])
    if((serverMsgStr == "00") or (serverMsgStr == "40")or (serverMsgStr == "24")):
        imageDataStore[frameRef] = rawMsg[12 : 41]
        display.show(Image(imageDataStore[frameRef]))
        return

    if(totalFrames == 0): return

    if((serverMsgStr == "20") or (serverMsgStr == "41")):
        frameBufferRef = (frameRef + getColRef()) % totalFrames
        imageDataStore[frameBufferRef ] = rawMsg[12 : 41]
        display.show(Image(imageDataStore[frameBufferRef]))


def processServerInstruction(rawMsg):
    global pauseShowFrame
    global totalFrames
    global frameSpeed
    
    instructionType = int(rawMsg[3 : 5])
    print(str(instructionType))
    if(instructionType == 99): reset()
    if(instructionType == 90): checkBufferSize()    
    if(instructionType == 60): setNodeRowAndCol(rawMsg[5 : 7], rawMsg[7 : 9])
    if(instructionType == 61): totalFrames = int(rawMsg[5:9])
    if(instructionType == 62): updateAnimationParams(1, 1)
    if(instructionType == 63): updateAnimationParams(-1, 1)
    if(instructionType == 66): frameSpeed = int(rawMsg[5 : 9])
    if(instructionType == 67): updateAnimationParams(1, 0)
    if(instructionType == 68): updateAnimationParams(-1, 0)
    if(instructionType == 80): pauseShowFrame = True
    if(instructionType == 81): pauseShowFrame = False
    if(instructionType == 82): setSynchFrame(int(rawMsg[5:9]), 0)
    if(instructionType == 83): setSynchFrame(int(rawMsg[5:9]), nodeID) 
        
    if((instructionType == 21) and (int(rawMsg[9 : 12]) == getRowRef())):    updateAnimationParams(1, 1)
    if((instructionType == 22) and (int(rawMsg[9 : 12]) == getRowRef())):    updateAnimationParams(-1, 1)


def checkBufferSize():
    bufferFull = True
    for i in range(0, totalFrames, 1):
        if(imageDataStore[i] == ""):    bufferFull = False

    if(bufferFull):     display.show(Image("00000:00009:00090:90900:09000"))
    else:               display.show("X")


def updateAnimationParams(aDirection, aType):
    global animationDirection    
    global animationType
    animationDirection = aDirection
    animationType = aType
    

def setSynchFrame(synchFrame, frameOffset):
    global currentFrame
    global scrollIndex
    currentFrame = synchFrame 
    currentFrame = getAdjacentFrameIndex(frameOffset)
    scrollIndex = 0


def setNodeRowAndCol(rowStr, colStr):
    global totalRows
    global totalCols
    totalRows = int(rowStr)
    totalCols = int(colStr)


def getColRef():
    return(int(nodeID % totalCols))

def getRowRef():
    return int((nodeID - getColRef()) / totalCols)


def showNextFrame():
    global currentFrame
    if(animationType == 0):   
        currentFrame = getAdjacentFrameIndex(animationDirection)
        display.show(Image(imageDataStore[currentFrame]))    
    else:
        display.show(Image(makeNextScrollFrame()))    


def makeNextScrollFrame():
    global scrollIndex
    global currentFrame
    global totalCols
    global animationDirection
    
    scrollIndex = scrollIndex + animationDirection
    if((scrollIndex > 4) or (scrollIndex < 0)): currentFrame = getAdjacentFrameIndex(animationDirection)
    scrollIndex = scrollIndex % 5

    if(scrollIndex == 0): return imageDataStore[currentFrame]

    nextFrame = getAdjacentFrameIndex(animationDirection)

    # 09090:90909:90009:09090:00900... 0, 6, 12, 18, 24
    scrollImageData = ""
    for i in range(0, 5, 1):
        scrollImageData = scrollImageData + imageDataStore[currentFrame][(i*6) + scrollIndex : (i*6) + 5] + imageDataStore[nextFrame][(i*6) : (i*6) + scrollIndex]
        if(i < 4): scrollImageData = scrollImageData + ":"
    return scrollImageData


def getAdjacentFrameIndex(frameIncrement):
    return (int( (currentFrame + frameIncrement) % totalFrames))


while True:
    sleep(10)
    processServerMessage(getServerMessage())
    
    if not(pauseShowFrame):     
        showNextFrame()
        sleep(frameSpeed - 10)

