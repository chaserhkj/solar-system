import Display
import galaxy
import math
from PyQt4.QtGui import QApplication

array = galaxy.celaArray(20)
size=[14]
sun = galaxy.cela(0, galaxy.vector(0,0,0), galaxy.vector(0,0,0),1000000,1,"Sun")
array[0] = sun
for i in xrange(1,10):
    array[i] = galaxy.cela(i, galaxy.vector(40*i,0,0),
            galaxy.vector(0,math.sqrt(2500/i),i),1,1,"Earth"+str(i))
    size.append(6)
array[10]=galaxy.cela(11, galaxy.vector(60,0,0),
        galaxy.vector(0,0,55),0.1,1,"Comet")
size.append(4)
g = galaxy.galaxy(11, array, 0.01, G=0.1, r=6, o=0.1, aplfx=False)

app = QApplication([])
d = Display.DisplayWidget(g,size ,scale=400,plane_scale =
        600,cell_density=20)
d.show()
d.start()
#d.toggleFullScreen()
app.exec_()
