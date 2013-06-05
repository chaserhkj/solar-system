This program is licensed under the MIT license.
See LICENSE.txt for more about license.

To build this program, you need:
python 2 with pyqt support
Qt4 with OpenGL support
Then issue command "make".

To create or modify a system, run:
python2 dist/Editor.py

To launch a system from a json file, run:
python2 dist/Launcher.py

Controls:
Hold left mouse button and drag: circle view
Hold right mouse button and drag: move view
Mouse scroll: zoom in/out
Q: quit
F:toggle fullscreen
T:trace next object
G:trace previous object
Z:quit tracing mode
X:trace on/off
WASD:move view
YU:move view along X-asix
HJ:move view along Y-asix
NM:move view along Z-asix
-=:zoom in/out
Ctrl + -=:change the distance between viewpoint and axes center
/:set view to default
O:fix system energy to startup
P:toggle energe fix
,.:decrease/increase speed
;:set speed to default
Esc:quit fullscreen/quit program


