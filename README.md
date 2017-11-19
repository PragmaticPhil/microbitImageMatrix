
# microbitImageMatrix
A client microbit serves image data, metadata and instructions to nodes.
Nodes are microbits in a matrix.
... these nodes are flashed with the mbImageService_Node.py code
... each node has a hardcoded ID (int).  This value is sequential, and runs from 0 to (number of nodes - 1)
Nodes do not contains any image data - they display images pass over radion by the server.

The purpose of this app is to allow a single micro:bit to control the visual output of a matrix of other micro:bits.
In theory one server could control a very large number of nodes.
In addition, you could have several servers all controlling the same matrix.

Atm ALL server code in Master is just throw away test code.
Ultimately I intend to build the real server in Excel:
... this will comm via serial with a single micro:bit, which will relay the instruction via radio to the nodes.
I still need to work out exactly how to this though!

One goal of this app is to be flexible:  to allow a server to control multiple different shapes (i.e. row x col)
of nodes without needing to recode / reflash the nodes.  This has been achieved.

Setup:
... there is NO wiring
... every micro:bit is powered by a battery
... communication between micro:bits is done by radio.

Key Points:
... each node has a buffer of up to 10 images.  Data is flashed by the server and nodes fill their buffers with this data
... buffers can be refreshed in real time, and nodes can play through their buffers.
... ... 'Animation' = nodes show buffers sequentially
... ... 'Scrolling' = nodes transition smoothly from 1 frame to the next.

Overview of Functionality:
... The 'server' will contain image data:
... ... this image data could be for a 'high' resolution (say 125x100 pixels).  This could be used as a back-drop.  Sprites or suchlike could then be drawn on the back-drop.
... ... simple animations can also be supported, as can scrolling.
... A number of 'nodes' will listen for instructions from the server.
... Each node will occupy a given space in 2d (row, column)
... The server will break down the large image into chunks and will serve them up to each node
... The node will display the image served up.

So, the server will send image data and instructions to the nodes
Image data is basically 25 values between 0 and 9.
Nodes will contain a buffer of images - 10 is current working # but larger buffer = mode control.
Server issues instructions to nodes, controlling a variety of functionality (see Node_InstructionList in master).

HOW TO MAKE IT WORK:
You need at least 2 micro:bits
1... on the first one flash mbImageService_Node.py.  Check the hardcoded ID (should be 0).  
This is your node
2... on the second one flash serverTest_animate_xFrames.py
This server will provide image data to the node.
Just click button A or button B to transmit image data.
3... you will also need to flash serverTest_animate.py
this server will send animation instructions to the node
Button A toggles pause and button b runs through the 4 different animation options.

NB - if you only have 2 micro:bits you can do the following:
1:
... Flash serverTest_animate_xFrames.py onto the server, then click A or B to transmit image data to the node.

