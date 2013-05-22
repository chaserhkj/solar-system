#!/usr/bin/env python2
import PyQt4.QtOpenGL as qgl
import OpenGL.GL as gl
import OpenGL.GLUT as glut

class DisplayWidget(qgl.QGLWidget):
    def __init__(self, galaxy, scale, timeout = 100, parent = None):
        qgl.QGLWidget.__init__(self, parent)
        self.setWindowTitle("Demo")
        self.setFixedSize(500,500)

#        self._galaxy = galaxy

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glColor3f(0.6,0.8,1.0)
        gl.glBegin(gl.GL_POINTS)
        gl.glVertex2f(0,0)
        gl.glVertex2f(0,0.1)
        gl.glVertex2f(0,0.2)
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
        
        
# from PyQt4.QtGui import QApplication
# app = QApplication([])
d = DisplayWidget()
d.show()
