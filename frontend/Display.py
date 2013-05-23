#!/usr/bin/env python2
import PyQt4.QtOpenGL as qgl
import PyQt4.QtCore as c
import PyQt4.QtGui as g
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
import cmath
import galaxy

class ValueDisplayWidget(g.QWidget):
    def __init__(self, galaxy_obj, parent=None):
        g.QWidget.__init__(self,parent)

        self._galaxy = galaxy_obj
        self._t = g.QLabel("", self)
        self._e = g.QLabel("",self)

        self._layout = g.QVBoxLayout()
        self._layout.addWidget(self._t)
        self._layout.addWidget(self._e)
        self.setLayout(self._layout)
        
        self.updateValue()
        
    def updateValue(self):
        self._t.setText("Time: %s"%str(self._galaxy.getTime()))
        self._e.setText("Energy: %s"%str(self._galaxy.getEnergy()))
        
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

        self._vDisplay = ValueDisplayWidget(self._galaxy, self)
            
        self._timer = c.QTimer(self)
        self._timer.timeout.connect(self.run)
        self._timer.timeout.connect(self._vDisplay.updateValue)
        
        self._fs = False
        self._n = self._galaxy.getCelaNum()

        self._fs_sc = g.QShortcut("f",self)
        self._fs_sc.activated.connect(self.toggleFullScreen)

        self._exit_sc1 = g.QShortcut("q",self, self.close)
        self._exit_sc2 = g.QShortcut("Esc",self, self._esc_handler)

        self._zoomin_sc = g.QShortcut("=",self, self._zoomin)
        self._zoomout_sc = g.QShortcut("-",self, self._zoomout)

        self._upa_sc = g.QShortcut("Up", self, self._moveupa)
        self._downa_sc = g.QShortcut("Down", self, self._movedowna)
        self._lefta_sc = g.QShortcut("Left", self, self._movelefta)
        self._righta_sc = g.QShortcut("Right", self, self._moverighta)
        self._rin_sc = g.QShortcut("Ctrl+=",self, self._rin)
        self._rout_sc = g.QShortcut("Ctrl+-",self, self._rout)
        
        self._up_sc = g.QShortcut("w", self, self._moveup)
        self._down_sc = g.QShortcut("s", self, self._movedown)
        self._left_sc = g.QShortcut("a", self, self._moveleft)
        self._right_sc = g.QShortcut("d", self, self._moveright)
        
        self._inx_sc = g.QShortcut("y", self, self._inx)
        self._dex_sc = g.QShortcut("u", self, self._dex)
        self._iny_sc = g.QShortcut("h", self, self._iny)
        self._dey_sc = g.QShortcut("j", self, self._dey)
        self._inz_sc = g.QShortcut("n", self, self._inz)
        self._dez_sc = g.QShortcut("m", self, self._dez)

        self._trace_f_sc = g.QShortcut("t", self, self._trace_f)
        self._trace_b_sc = g.QShortcut("g", self, self._trace_b)

        self._reset_sc = g.QShortcut("/", self, self._reset_view)
        
        self._trace = -1

        self._reset()

    def _reset(self):
        
        self._view_angle = 30
        
        self._x = 0
        self._y = 0
        self._dx = 0
        self._dy = 0
        self._dz = 0
        self._rho = 3
        self._theta = 45
        self._phi = 45

    def _reset_view(self):
        self._reset()
        self.makeCurrent()
        self.setCamera()
        
    def _trace_f(self):
        self._trace = self._trace + 1
        if self._trace == self._n:
            self._trace = -1

    def _trace_b(self):
        self._trace = self._trace - 1
        if self._trace == -2:
            self._trace = self._n - 1
            
    def _inx(self):
        self._dx = self._dx + 0.05
        self.makeCurrent()
        self.setCamera()
        
    def _dex(self):
        self._dx = self._dx - 0.05
        self.makeCurrent()
        self.setCamera()
        
    def _iny(self):
        self._dy = self._dy + 0.05
        self.makeCurrent()
        self.setCamera()
        
    def _dey(self):
        self._dy = self._dy - 0.05
        self.makeCurrent()
        self.setCamera()
        
    def _inz(self):
        self._dz = self._dz + 0.05
        self.makeCurrent()
        self.setCamera()
        
    def _dez(self):
        self._dz = self._dz - 0.05
        self.makeCurrent()
        self.setCamera()
        
    def _esc_handler(self):
        if self._fs:
            self.toggleFullScreen()
        else:
            self.close()
            
    def _moveup(self):
        self._y = self._y - 0.05  
        self.makeCurrent()
        self.setCamera()

    def _movedown(self):
        self._y = self._y + 0.05
        self.makeCurrent()
        self.setCamera()

    def _moveleft(self):
        self._x = self._x + 0.05
        self.makeCurrent()
        self.setCamera()

    def _moveright(self):
        self._x = self._x - 0.05
        self.makeCurrent()
        self.setCamera()
    
        
        
    def _rin(self):
        self._rho = self._rho - 0.5
        self.makeCurrent()
        self.setCamera()
        
        
    def _rout(self):
        self._rho = self._rho + 0.5
        self.makeCurrent()
        self.setCamera()

    def _moveupa(self):
        self._theta = self._theta - 1
        self.makeCurrent()
        self.setCamera()

    def _movedowna(self):
        self._theta = self._theta + 1
        self.makeCurrent()
        self.setCamera()
        
    def _movelefta(self):
        self._phi = self._phi - 1
        self.makeCurrent()
        self.setCamera()

    def _moverighta(self):
        self._phi = self._phi + 1
        self.makeCurrent()
        self.setCamera()
            
    def _zoomin(self):
        self._view_angle = self._view_angle - 2
        self.makeCurrent()
        self.setCamera()
        
    def _zoomout(self):
        self._view_angle = self._view_angle + 2
        self.makeCurrent()
        self.setCamera()

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

        array = galaxy.\
                celaArray_frompointer(self._galaxy.\
                                      output())
        if self._trace >= 0:
            self._dx = array[self._trace].p.x * self._scale_factor
            self._dy = array[self._trace].p.y * self._scale_factor
            self._dz = array[self._trace].p.z * self._scale_factor
            self.setCamera()
        
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

        for i in xrange(self._n):
            gr = self._grs[i]
            gl.glPushMatrix()
            gl.glTranslate(array[i].p.x,
                           array[i].p.y,
                           array[i].p.z)
            glut.glutWireSphere(gr, 8, 8)
            gl.glPopMatrix()

    def setTraceCela(self,celaN):
        if celaN < -1 or celaN >= self._n :
            raise ValueError

        self._trace = celaN

    def initializeGL(self):
        glut.glutInit([])
        gl.glClearColor(0,0,0,0)
        gl.glShadeModel(gl.GL_FLAT)

    def setCamera(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(self._view_angle, self._aspect, 0, 100)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glTranslate(self._x, self._y, 0)
        glu.gluLookAt(self._rho * cmath.sin(self._theta /180.0 * cmath.pi).real * cmath.cos(self._phi /180.0 * cmath.pi).real + self._dx,
                      self._rho * cmath.sin(self._theta /180.0 * cmath.pi).real * cmath.sin(self._phi /180.0 * cmath.pi).real + self._dy,
                      self._rho * cmath.cos(self._theta /180.0 * cmath.pi).real + self._dz,
                      self._dx, self._dy, self._dz,
                      0, 0, 1)
        gl.glScale(self._scale_factor,
                   self._scale_factor,
                   self._scale_factor)

        
    def resizeGL(self, w, h):
        gl.glViewport(0, 0, w, h)
        self._aspect = float(w)/float(h)
        self.setCamera()

        
