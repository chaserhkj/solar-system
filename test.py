import Display
import galaxy
from PyQt4.QtGui import QApplication

sun = galaxy.cela(0, galaxy.vector(0,0,0), galaxy.vector(0,0,0),1,0.001,"Sun")
earth = galaxy.cela(0, galaxy.vector(10,0,0), galaxy.vector(0,1,0),0.01,0.001,"Earth")
array = galaxy.celaArray(2)
array[0] = sun
array[1] = earth
g = galaxy.galaxy(2, array, 0.1, 10)

app = QApplication([])
d = Display.DisplayWidget(g,[0.5, 0.5] ,10,plane_scale = 20)
d.show()
d.start()
app.exec_()
