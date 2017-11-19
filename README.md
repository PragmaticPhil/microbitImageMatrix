# microbitImageMatrix
A client microbit serves image data, metadata and instructions to nodes.
Nodes are microbits in a matrix.
Nodes do not contains any image data - they display images pass over radion by the server.

The purpose of this app is to allow a single micro:bit to control the visual output of a matrix of other micro:bits.
In theory one server could control a very large number of nodes.
In addition, you could have several servers all controlling the same matrix.

ALL server code in Master is just throw away test code.
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
Nodes will contain a buffer of images - total will depend on how much memory we have to play with.  10 is current working #
Instructions will allow for (e.g) transitional effects.

Nodes:
Each node will have the following:
... store some global variables
... recieve radio signals
... identify server radio signals and interpret them
... send radio signals (e.g. request for resend if checksums dont match)
... show an image on screen
... prepare an image buffer (for transitions)


Servers:
UI will be built, ultimately in Excel (cos I love Excel and have always wanted to do something with both techs I love!)
... This will allow images to be entered into the server
... It will also allow the user to animate and manipulate the matrix.
The server will:
... have a concept of a matrix space that it controls (x, y)
... record the name (UID) and location (x, y) of every node in its remit
... have access to image data that is 'high' resolution data (presumably compatible with (x, y) )
... have access to user instructions to determine how the image data is displayed (scroll left, scoll right, flash etc)
As well as being able to:
... break a raw 'high res' image down into 5x5 micro:bit sized chunks
... serve up these chunks to nodes on the matrix
... server up instructions to the nodes

BUT - server code is long term... the version you are looking at has a very basic server, which is little more
than test code.  



