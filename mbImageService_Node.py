from microbit import*
import radio
radio.on()
radio.config(length=50, queue=11, channel=11, power=6)

nodeID = 0
global totalRows
global totalCols
global rowRef
global colRef
rowRef = 0
colRef = nodeID
totalRows = 1
totalCols = nodeID + 1

global currentFrame
currentFrame = 0

global scrollIndex
global scrollDirection
scrollIndex = 0
scrollDirection = 0

global animationDirection
animationDirection = 1

global pauseShowFrame
pauseShowFrame = True

global frameSpeed
frameSpeed = 250

global imageDataStore
imageDataStore = [(""),(""),(""),(""),(""),(""),(""),(""),(""),(""),]
global totalFrames
totalFrames = 10

def getServerMessage():
    try:        return str(radio.receive())
    except:     return "X"


def processServerMessage(rawMsg):
    if(len(rawMsg) < 5):                return
    if(not(rawMsg[0 : 2] == "pX")):     return
    print("Valid msg: " + rawMsg)
    if(rawMsg[2 : 3] == "0"):                   processServerInstruction(rawMsg)
    else:                               
        if(isRelevantImageMessage(rawMsg)):     processImageMessage(rawMsg)


def isRelevantImageMessage(rawMsg):
#    try:
    if(not(rawMsg[2 : 3] == "1")):                                      return False
    if((rawMsg[3 : 5] == "00") and (int(rawMsg[9 : 12]) == nodeID)):    return True
    if((rawMsg[3 : 4] == "2") and (int(rawMsg[9 : 12]) == rowRef)):     return True
    return False
#    except:


def processImageMessage(rawMsg):
    global imageDataStore
    imageStr = rawMsg[12 : 41]
    serverMsgStr = rawMsg[3 : 5]
    frameRef = int(rawMsg[5 : 9])
    print("Processing image")
    if(serverMsgStr == "00"):
        imageDataStore[frameRef] = imageStr
        print("Inserting image into buffer - " + str(frameRef))
        display.show(Image(imageDataStore[frameRef]))
        return

    if(totalFrames == 0): return

    if(serverMsgStr == "20"):          
        frameBufferRef = (frameRef + colRef) % totalFrames
        print("FrameBufferRef = " + str(frameBufferRef))
        imageDataStore[frameBufferRef ] = imageStr
        display.show(Image(imageDataStore[frameBufferRef]))


def processServerInstruction(rawMsg):
    global pauseShowFrame
    global scrollDirection
    global totalFrames
    global frameSpeed
    
    instructionType = int(rawMsg[3 : 5])
    print("Server instruction = " + str(instructionType))
    if(instructionType == 99): reset()
    if(instructionType == 90): checkBufferSize()    
    if(instructionType == 60): setNodeRowAndCol(rawMsg[5 : 7], rawMsg[7 : 9])
    if(instructionType == 61): totalFrames = int(rawMsg[5:9])
    if(instructionType == 62): scrollDirection = 1
    if(instructionType == 63): scrollDirection = -1
    if(instructionType == 66): frameSpeed = int(rawMsg[5:9])
    if(instructionType == 67): setAnimationDirection(1)
    if(instructionType == 68): setAnimationDirection(-1)
    if(instructionType == 80): pauseShowFrame = True
    if(instructionType == 81): pauseShowFrame = False
    if(instructionType == 82): setSynchFrame(int(rawMsg[5:9]), 0)
    if(instructionType == 83): setSynchFrame(int(rawMsg[5:9]), nodeID) 
        
    if((instructionType == 21) and (int(rawMsg[9 : 12]) == rowRef)):    scrollDirection = 1
    if((instructionType == 22) and (int(rawMsg[9 : 12]) == rowRef)):    scrollDirection = -1


def checkBufferSize():
    bufferFull = True
    for i in range(0, totalFrames, 1):
        if(imageDataStore[i] == ""):    bufferFull = False

    if(bufferFull):     display.show(Image("00000:00009:00090:90900:09000"))
    else:               display.show(Image("90009:09090:00900:09090:90009"))


def setAnimationDirection(newDir):
    global scrollDirection
    global animationDirection
    animationDirection = newDir
    if(not(animationDirection == 0)): scrollDirection = 0
    

def setSynchFrame(synchFrame, frameOffset):
    global currentFrame
    global scrollIndex
    currentFrame = synchFrame 
    currentFrame = getAdjacentFrameIndex(frameOffset)
    scrollIndex = 0


def setNodeRowAndCol(rowStr, colStr):
    global totalRows
    global totalCols
    global rowRef
    global colRef

    totalRows = int(rowStr)
    totalCols = int(colStr)
    colRef = int(nodeID % totalCols)
    rowRef = int((nodeID - colRef) / totalCols)


def showNextFrame():
    global currentFrame
    if(scrollDirection == 0):   
        currentFrame = getAdjacentFrameIndex(animationDirection)
        display.show(Image(imageDataStore[currentFrame]))    
    else:
        display.show(Image(makeNextScrollFrame()))    


def makeNextScrollFrame():
    global scrollIndex
    global currentFrame
    global totalCols
    global scrollDirection
    
    scrollIndex = scrollIndex + scrollDirection
    if((scrollIndex > 4) or (scrollIndex < 0)): currentFrame = getAdjacentFrameIndex(scrollDirection)
    scrollIndex = scrollIndex % 5

    if(scrollIndex == 0): return imageDataStore[currentFrame]

    nextFrame = getAdjacentFrameIndex(scrollDirection)

    # 09090:90909:90009:09090:00900... 0, 6, 12, 18, 24
    scrollImageData = ""
    for i in range(0, 5, 1):
        scrollImageData = scrollImageData + imageDataStore[currentFrame][(i*6) + scrollIndex : (i*6) + 5] + imageDataStore[nextFrame][(i*6) : (i*6) + scrollIndex]
        if(i < 4): scrollImageData = scrollImageData + ":"
    return scrollImageData


def getAdjacentFrameIndex(frameIncrement):
    return (int( (currentFrame + frameIncrement) % totalFrames))


#-------------------------------------------------------------------------------------------------------------------------

while True:
    sleep(10)
    processServerMessage(getServerMessage())
    
    if not(pauseShowFrame):     
        showNextFrame()
        sleep(frameSpeed - 10)

