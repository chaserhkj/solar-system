import Display
import galaxy
import math
from PyQt4.QtGui import QApplication

array = galaxy.celaArray(3)
sun = galaxy.cela(0, galaxy.vector(0,0,0), galaxy.vector(0,0,0),1000000,1,"Sun")
array[0] = sun
array[1]=galaxy.cela(1,
        galaxy.vector(400,0,0),galaxy.vector(0,math.sqrt(250),0),0.1,0,"Earth") 
array[2]=galaxy.cela(2, galaxy.vector(401,0,0),
        galaxy.vector(0,math.sqrt(250)+math.sqrt(0.01),0),0.001,0,"Moon")
size=[30,7,5]
g = galaxy.galaxy(3, array, step=0.01, G=0.1, t=0, r=6, o=0.1, aplfx=False)

app = QApplication([])
d = Display.DisplayWidget(g,size ,scale=400,plane_scale =
        600,cell_density=20)
d.show()
d.start()
#d.toggleFullScreen()
app.exec_()
