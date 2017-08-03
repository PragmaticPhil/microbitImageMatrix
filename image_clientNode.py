from microbit import*
import radio
radio.on()
radio.config(length=64, queue=8, channel=11, power=6)
# several nodes are attached to a server (its flexible)
# the server will provide each node with image data - telling it what to display
# server will also issue instructions about how to play that data (mostly which frame to display)
nodeID = 3

# FOR NOW we will hard code buffer at 9 frames, and set all to a default animation.
global imageDataStore
imageDataStore = [
("00000:00000:00000:00000:00000"),
("00000:02520:02820:02520:00000"),
("02520:05850:00800:05850:02520"),
("25825:05850:00800:05850:25852"),  
("99999:99999:99999:99999:99999"),
("25825:05850:00800:05850:25852"),
("02520:05850:00800:05850:02520"),  
("00000:02520:02820:02520:00000"),
("00000:00000:00000:00000:00000"),
]

# we are also going to hardcode a few utility images (WiP to allow 'compression' wrt msgs from server):
BLANK_SCREEN = "00000:00000:00000:00000:00000"
FULL_SCREEN = "99999:99999:99999:99999:99999"

#   there are several display modes:
#   0 = pause on current image. This mode effectively waits for instructions from server as to which frame to play.
#   1 = animate backward
#   2 = animate forwards
#   3 = show blank (clear screen)
global displayMode
displayMode = 0

# the server will send 2 types:
#
#   1:  Image data.  Each node gets a specific message with data to construct a 5x5 image.  Also metadata, including frame number (nb for animation)
#       e.g.    [meta][row1:row2:row3:row4:row5]
#               meta = [serverID, 3char][nodeID, 3char][serverInstruction, 2 char][InstructionParams, 4char][separator][image data] - 
#                   [InstructionParams = 0001] = tells node where to store the image data for later play-back.

#       e.g.   pXa013990001!90909:90909:90909:90909:90909
#              pXa = message from server with image data
#              013 = node to which msg is being broadcast
#              99  = instruction from server (save image, but irrelevant cos inferred from the a in pXa)
#              0001 = save the image in Frame 1 buffer 

#   2:  Server instructions.  Broadcast to all nodes simultaneously - usually instruction is "show frame 6".
#       e.g. [serverID, 3char][nodeID, 3char][serverInstruction, 2 char][InstructionParams, 4char]
#       e.g. pXb999020001
#       pXb = message from server with instruction
#       999 means all nodes
#       02 means instruction is show frame (other instructions include set frame delay)
#       0001 means show frame 01.

# each node will build up a number of buffers, which will allow for smooth rendering (albeit with long load times).
# buffers are stored as string arrays and are processed jit.

def getServerMessage():
    #display.show("k")
    #print("getServerMessage")
    try:
        serverMsg = str(radio.receive())        #   print(serverMsg)
        sleep(50)
        return serverMsg
    except:
        return "XXX"


def processServerInstruction(rawMsg):                       #   print("processServerInstruction" + rawMsg)
    if(rawMsg == "XXX"): return                             #   invalid message so ignore
    if(not isValidServerMessage(rawMsg)):    return         #   message is of NO relevance to this node so we just ignore.
    
    # If we are here then the message received is relevant to this node and needs to be processed.
    # First step is to identify instruction type:
    serverMessageType = getServerMessageType(rawMsg)    #print("valid servermsg in processServerInstruction - serverMessageType = " + str(serverMessageType))
    if(serverMessageType == 1):                         # server is sending a new image to add to buffer
        addImageToBuffer(rawMsg)
        return
    if(serverMessageType == 2):                         # server is sending an instruction
        showFrame(getFrameFromServerMsg(rawMsg))
        return
    # if not 1 or 2 then donothing


def isValidServerMessage(rawMsg):               #   is the radio message actually sent by the Server?
                                                #   print("isValidServerMessage: " + rawMsg)
    try:
        serverMsg = rawMsg[0 : 2]                # ALL messages from server are prefixed "pX"     #print("isValidServerMessage: " + serverMsg)
        if(serverMsg == "pX"):  return isRelevantServerMessage(rawMsg)  # message IS from server and IS aimed at this node.
        return False
    except:                                     #print("Exception in isValidServerMessage")
        return False

def isRelevantServerMessage(rawMsg):            #   the radio message DOES come from the server, but is it aimed at THIS node?
                                                #   print("isRelevantServerMessage")
    try:
        serverMsg = rawMsg[3 : 6]                # nodeID is always chars [3, 6] (3 chars) in radio message   #print("target node = " + serverMsg)
        nodeTarget = int(serverMsg)             # that string of chars are always integers (but use error trapping just in case!)
        if(nodeTarget == 999 or nodeTarget == nodeID):  return True     # 999 are instructions to ALL nodes
        return False
    except:
        return False
    

def getServerMessageType(rawMsg):           # is the server sending new image data, or instructions on what / how to display images?
    try:
        serverMsg = rawMsg[2]                # server message type is encoded in 3rd char
        #print("getServerMessageType str = " + serverMsg)
        if(serverMsg == "a"):
            return 1
        if(serverMsg == "b"):  
            return 2    
        return 0
    except:
        #print("Exception in getServerMessageType")
        return 0

def addImageToBuffer(rawStr):
    global imageDataStore                               # will write directly to buffer
    targetFrame = getFrameFromServerMsg(rawStr)         # will always return a valid frame ref, so we won't check it here
    newImageData = getImageData(rawStr)
    print("newImageData  = " + newImageData)
    imageDataStore[targetFrame] = newImageData
    print("Image data store updated - frame = " + str(targetFrame))
        
def getImageData(rawStr):
    imageStr = ""
    try:
        imageStr = rawStr[13 : 42]                  #   print("image data = " + imageStr)
        return imageStr
    except:                                         #   print("getImageData - EXCEPTION")
        return BLANK_SCREEN                         #   When error thrown blank screen is added.


def getFrameFromServerMsg(rawMsg):                # frame is encoded in chars 9, 10, 11 and 12 of the server message
    #print("getFrameFromServerMsg, rawmsg = " + rawMsg)
    try:
        frameStr = rawMsg[8 : 12]                   # print("Frame to show (str) = " + frameStr)
        frameInt = int(frameStr)                    # print("Frame to show (int) = " + str(frameInt))
        if(isValidFrame(frameInt)): return frameInt
        return 0
    except:                                         # print("getFrameFromServerMsg - EXCEPTION")
        return 0                                    # When in doubt frame 0 is shown

def isValidFrame(frameInt):                         # check ID is in range.  Image buffer size hard coded below at 9.
    return ((frameInt < 9) and (frameInt > -1))     # frame must be value between 0 and 8


def showFrame(frameID): 
    if(isValidFrame(frameID)):  display.show(Image(imageDataStore[frameID]))
    else:                       display.show("X")


while True:
    #display.show("i")
    sleep(50)
    processServerInstruction(getServerMessage())
    
       
