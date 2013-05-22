#!/usr/bin/env python2
import PyQt4.QtOpenGL as qgl
import PyQt4.QtCore as c
import OpenGL.GL as gl
# import OpenGL.GLUT as glut
import galaxy

class DisplayWidget(qgl.QGLWidget):
    def __init__(self,
                 galaxy_obj,
                 scale,
                 timeout = 100,
                 parent = None):
        qgl.QGLWidget.__init__(self, parent)
        self.setWindowTitle("Demo")
        self.setFixedSize(500,500)

        self._galaxy = galaxy_obj
        self._scale = float(scale)
        self._timeout = timeout

        self._timer = c.QTimer(self)
        self._timer.timeout.connect(self.run)
        
    def run(self):
        self._galaxy.run()
        self.updateGL()

    def start(self):
        self._timer.start(self._timeout)
        
    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glColor3f(0.6,0.8,1.0)
        N = self._galaxy.getCelaNum()
        gl.glBegin(gl.GL_POINTS)
        for i in xrange(N):
            array = galaxy.celaArray_frompointer(self._galaxy.output())
            x = array[i].p.x / self._scale
            y = array[i].p.y / self._scale
            # z = array[i].p.z / self._scale
            gl.glVertex2f(x, y)
        gl.glEnd()
        
    def initializeGL(self):
        # glut.glutInit([])
        gl.glClearColor(0,0,0,0)
        gl.glShadeModel(gl.GL_FLAT)
        
    def resizeGL(self, w, h):
        gl.glViewport(0, 0, w, h)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        
