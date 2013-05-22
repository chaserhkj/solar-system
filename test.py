import Display
import galaxy
from PyQt4.QtGui import QApplication

sun = galaxy.cela(0, galaxy.vector(0,0,0), galaxy.vector(0,0,0),1,"Sun")
earth = galaxy.cela(0, galaxy.vector(5,0,0), galaxy.vector(0,1,0),0.01,"Earth")
array = galaxy.celaArray(2)
array[0] = sun
array[1] = earth
g = galaxy.galaxy(2, array, 0.1)

app = QApplication([])
d = Display.DisplayWidget(g, 10, 1)
d.show()
d.start()
app.exec_()
