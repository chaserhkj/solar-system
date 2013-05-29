import Display
import galaxy
import math
from PyQt4.QtGui import QApplication

array = galaxy.celaArray(20)
graphic=[{"radius":14,"color":[1,0,0]}]
sun = galaxy.cela(0, galaxy.vector(0,0,0), galaxy.vector(0,-5,0),1000000,1,"Sun")
array[0] = sun
for i in xrange(1,10):
    array[i] = galaxy.cela(i, galaxy.vector(40*i,0,0),
            galaxy.vector(0,math.sqrt(2500/i),i),1,1,"Earth"+str(i))
    graphic.append({"radius":6,"color":[1-0.08*i,1-0.05*i+0.1,0]})
array[10]=galaxy.cela(11, galaxy.vector(60,0,0),
        galaxy.vector(0,5,30),1000000,1,"Comet")
graphic.append({"radius":4,"color":[0,0,1]})
g = galaxy.galaxy(11, array, step=0.01, G=0.1, t=0, r=69, o=0.01, aplfx=False)

app = QApplication([])
d = Display.DisplayWidget(g,graphic ,scale=400,light = True,line_width = 1,multisampling = True,smooth = 0,plane_scale =
        600,cell_density=20,interval=20,shadow_line = True,  line_interval=1, trace_buffer=50)
d.show()
#d.start()
app.exec_()
