#!/usr/bin/env python2
import PyQt4.QtOpenGL as qgl
import PyQt4.QtCore as c
import PyQt4.QtGui as g
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
import galaxy

class DisplayWidget(qgl.QGLWidget):
    def __init__(self,
                 galaxy_obj,
                 gradius_list,
                 scale,
                 step_count = 10,
                 interval = 20,
                 plane_scale = None,
                 cell_density = 10,
                 parent = None):
        qgl.QGLWidget.__init__(self, parent)
        self.setWindowTitle("Demo")
        self.resize(500,500)

        self._galaxy = galaxy_obj
        self._grs = gradius_list
        self._scale_factor = float(1)/float(scale)

        self._stepc = step_count
        self._interval = interval

        if plane_scale == None:
            self._planes = scale
        else:
            self._planes = plane_scale
            self._celld = cell_density

        
        self._timer = c.QTimer(self)
        self._timer.timeout.connect(self.run)

        self._fs = False

        self._fs_sc = g.QShortcut("f",self)
        self._fs_sc.activated.connect(self.toggleFullScreen)

        self._exit_sc1 = g.QShortcut("q",self)
        self._exit_sc1.activated.connect(self.close)
        self._exit_sc2 = g.QShortcut("Esc",self)
        self._exit_sc2.activated.connect(self.close)
        
        
    def run(self):
        for i in xrange(self._stepc):
            self._galaxy.run()
            self.updateGL()

    def toggleFullScreen(self):
        if self._fs:
            self.showNormal()
        else:
            self.showFullScreen()
        self._fs = not self._fs
            
    def start(self):
        self._timer.start(self._interval)
        
    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glColor(0.6,0.8,1.0)

        step = self._planes / float(self._celld)
        for i in xrange(2 * self._celld):
            gl.glBegin(gl.GL_LINES)
            gl.glVertex(- self._planes + i*step,
                        - self._planes)
            gl.glVertex(- self._planes + i*step,
                        self._planes - step)
            gl.glEnd()
        for i in xrange(2 * self._celld):
            gl.glBegin(gl.GL_LINES)
            gl.glVertex(- self._planes,
                        - self._planes + i*step)
            gl.glVertex(self._planes - step,
                        - self._planes + i*step)
            gl.glEnd()

        N = self._galaxy.getCelaNum()
        array = galaxy.\
                celaArray_frompointer(self._galaxy.\
                                      output())
        for i in xrange(N):
            gr = self._grs[i]
            gl.glPushMatrix()
            gl.glTranslate(array[i].p.x,
                           array[i].p.y,
                           0)
            glut.glutWireSphere(gr, 10, 10)
            gl.glPopMatrix()
            
    def initializeGL(self):
        glut.glutInit([])
        gl.glClearColor(0,0,0,0)
        gl.glShadeModel(gl.GL_FLAT)
        
    def resizeGL(self, w, h):
        gl.glViewport(0, 0, w, h)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(30, float(w)/float(h), 0, 100)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        glu.gluLookAt(2, 2, 2, -1, -1 ,-1, -1 , -1, 0)
        gl.glScale(self._scale_factor,
                   self._scale_factor,
                   self._scale_factor)
