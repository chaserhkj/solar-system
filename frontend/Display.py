#!/usr/bin/env python2
import PyQt4.QtOpenGL as qgl
import PyQt4.QtCore as c
import PyQt4.QtGui as g
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
import math, array
import galaxy

class ValueDisplayWidget(g.QWidget):
    def __init__(self, galaxy_obj, timer, trace ,parent=None):
        g.QWidget.__init__(self,parent)

        self._galaxy = galaxy_obj
        self._t = g.QLabel("")
        self._e = g.QLabel("")

        self._layout = g.QVBoxLayout()
        self._layout.addWidget(self._t)
        self._layout.addWidget(self._e)

        self._no = g.QLabel("")
        self._x = g.QLabel("")
        self._y = g.QLabel("")
        self._z = g.QLabel("")
        self._vx = g.QLabel("")
        self._vy = g.QLabel("")
        self._vz = g.QLabel("")
        self._layout.addWidget(self._no)
        self._layout.addWidget(self._x)
        self._layout.addWidget(self._y)
        self._layout.addWidget(self._z)
        self._layout.addWidget(self._vx)
        self._layout.addWidget(self._vy)
        self._layout.addWidget(self._vz)

        timer.timeout.connect(self.updateValue)
        
        self._trace = trace
        self.setLayout(self._layout)
        self.updateValue()

        self.setWindowTitle("Monitor")
        
    def setTrace(self, trace):
        self._trace = trace
        
    def updateValue(self):
        if self._trace == -1:
            self._no.setText("Tracing disabled.")
            self._x.setText("Object count: %s"%self._galaxy.getCelaNum())
            self._y.setText("Gravity constant: %s"%self._galaxy.getG())
            self._z.setText("Calculation step: %s"%self._galaxy.getStep())
            self._vx.setText("Recursive depth: %s"%self._galaxy.getRecDpt())
            self._vy.setText("Recursive coefficient: %s"%self._galaxy.getOmega())
            self._vz.setText("Fix applied: %s"%self._galaxy.appliedfix())
        else:
            _array = galaxy.celaArray_frompointer(self._galaxy.output())
            if _array[self._trace].name == "":
                name = "No. %s"%self._trace
            else:
                name = _array[self._trace].name
            self._no.setText("Tracing object: %s"%name)
            self._x.setText("X: %s"%_array[self._trace].p.x)
            self._y.setText("Y: %s"%_array[self._trace].p.y)
            self._z.setText("Z: %s"%_array[self._trace].p.z)
            self._vx.setText("Vx: %s"%_array[self._trace].v.x)
            self._vy.setText("Vy: %s"%_array[self._trace].v.y)
            self._vz.setText("Vz: %s"%_array[self._trace].v.z)
        self._t.setText("Time: %s"%self._galaxy.getTime())
        self._e.setText("Energy: %s"%self._galaxy.getEnergy())
        
class DisplayWidget(qgl.QGLWidget):
    def __init__(self,
                 galaxy_obj,
                 graphic_obj,
                 scale,
                 step_count = 10,
                 interval = 20,
                 trace_buffer = 1000,
                 plane_scale = None,
                 plane_color = [0.6,0.8,1.0],
                 cell_density = 10,
                 axis_length = None,
                 axis_color = [1, 1 ,1],
                 shadow_line = False,
                 line_interval = 5,
                 line_width = 1,
                 light = False,
                 default_style = "wired",
                 smooth = 0,
                 multisampling = False,
                 parent = None):
        qgl.QGLWidget.__init__(self, parent)
        self.setWindowTitle("Display")
        self.resize(500,500)
        
        self._galaxy = galaxy_obj
        self._graphic = graphic_obj
        self._scale = scale
        self._scale_factor = float(1)/float(scale)

        self._stepc = step_count
        self._interval = interval
        self._trace_buffer_size = trace_buffer * 3

        if plane_scale == None:
            self._planes = scale
        else:
            self._planes = plane_scale
            self._celld = cell_density
        self._planec = plane_color

        if axis_length == None:
            self._axisl = cell_density
        else:
            self._axisl = axis_length
        self._axisc = axis_color
        self._shadow = shadow_line
        self._line_int = line_interval

        self._linew = line_width
        self._multisample = multisampling
        self._smooth = smooth
        self._light = light
        self._dstyle = default_style
        
        fmt = qgl.QGLFormat()

        if multisampling:
            fmt.setSampleBuffers(True)

        self.setFormat(fmt)
            
        self._timer = c.QTimer(self)
        self._timer.timeout.connect(self.run)
        
        self._fs = False
        self._n = self._galaxy.getCelaNum()

        self._trace_buffer = []
        for i in xrange(self._n):
            self._trace_buffer.append(array.array("d"))
        
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
        self._trace_v_sc = g.QShortcut("b", self, self.toggleTraceV)
        self._trace_quit_sc = g.QShortcut("z", self,self._trace_quit)
        self._trace_line_sc = g.QShortcut("x",self, self._trace_line_handler)
        
        self._reset_sc = g.QShortcut("/", self, self._reset_view)
        
        self._pause_sc = g.QShortcut("Space", self, self.togglePaused)

        self._togglefix_sc = g.QShortcut("p", self, self._galaxy.togglefix)
        self._fixenergyto0_sc = g.QShortcut("o", self, self._galaxy.fixenergyto0)
        
        self._trace = -1
        self._trace_v = False
        self._trace_line = False

        self._vDisplay = ValueDisplayWidget(self._galaxy, self._timer, self._trace,self)
        self._vDisplay.setGeometry(0,0,165,190)
        
        self._mouse_moving = -1
        
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

    def getCelas(self):
        output = []
        array = galaxy.celaArray_frompointer(self._galaxy.output())
        for i in xrange(self._n):
            output.append(array[i])
        return output

    def getCelaNum(self):
        return self._n

    def getTime(self):
        return self._galaxy.getTime()
        
    def _reset_view(self):
        self._reset()
        self._updateCamera()
        
    def _clear_trace_buffer(self):
        del self._trace_buffer
        self._trace_buffer = []
        for i in xrange(self._n):
            self._trace_buffer.append(array.array("d"))

    def _trace_line_handler(self):
        self._trace_line = not self._trace_line
        self._clear_trace_buffer()
        self.updateGL()
        
    def _trace_f(self):
        self._clear_trace_buffer()    
        self._trace = self._trace + 1
        if self._trace == self._n:
            self._trace = -1
        self._vDisplay.setTrace(self._trace)
        self.updateGL()
        self._vDisplay.updateValue()

    def _trace_b(self):
        self._clear_trace_buffer()
        self._trace = self._trace - 1
        if self._trace == -2:
            self._trace = self._n - 1
        self._vDisplay.setTrace(self._trace)
        self.updateGL()
        self._vDisplay.updateValue()

    def _trace_quit(self):
        self._clear_trace_buffer()
        self._trace = -1
        self._vDisplay.setTrace(self._trace)
        self.updateGL()
        self._vDisplay.updateValue()
        
    def _inx(self):
        self._dx = self._dx + 0.05
        self._updateCamera()
        
    def _dex(self):
        self._dx = self._dx - 0.05
        self._updateCamera()
        
    def _iny(self):
        self._dy = self._dy + 0.05
        self._updateCamera()
        
    def _dey(self):
        self._dy = self._dy - 0.05
        self._updateCamera()

        
    def _inz(self):
        self._dz = self._dz + 0.05
        self._updateCamera()
        
    def _dez(self):
        self._dz = self._dz - 0.05
        self._updateCamera()
        
    def _esc_handler(self):
        if self._fs:
            self.toggleFullScreen()
        else:
            self.close()
            
    def _moveup(self):
        self._y = self._y - 0.05  
        self._updateCamera()

    def _movedown(self):
        self._y = self._y + 0.05
        self._updateCamera()

    def _moveleft(self):
        self._x = self._x + 0.05
        self._updateCamera()

    def _moveright(self):
        self._x = self._x - 0.05
        self._updateCamera()
        
    def _rin(self):
        step = 0.5
        if self._rho <= 1:
            step = self._rho / 10.0
        if self._rho - step < 1e-2:
            return
        self._rho = self._rho - step
        self._updateCamera()
        
    def _rout(self):
        step = 0.5
        if self._rho <= 1:
            step = self._rho / 10.0
        self._rho = self._rho + step
        self._updateCamera()

    def _moveupa(self):
        if self._theta - 1 < 0:
            return
        self._theta = self._theta - 1
        self._updateCamera()

    def _movedowna(self):
        if self._theta + 1 > 180:
            return
        self._theta = self._theta + 1
        self._updateCamera()
        
    def _movelefta(self):
        self._phi = self._phi - 1
        self._updateCamera()

    def _moverighta(self):
        self._phi = self._phi + 1
        self._updateCamera()
            
    def _zoomin(self):
        step = 1
        if self._view_angle <= 10:
            step = self._view_angle / 20.0
        if self._view_angle - step < 0:
            return
        self._view_angle = self._view_angle - step
        self._updateCamera()
        
    def _zoomout(self):
        step = 1
        if self._view_angle <= 10:
            step = self._view_angle / 10.0
        if self._view_angle + step > 180:
            return
        self._view_angle = self._view_angle + step
        self._updateCamera()
        
    def run(self):
        for i in xrange(self._stepc):
            self._galaxy.run()
        self.updateGL()

    def _updateCamera(self):
        self.makeCurrent()
        self.setCamera()
        self.updateGL()

    def toggleTraceV(self):
        self._trace_v = not self._trace_v
        
    def toggleFullScreen(self):
        if self._fs:
            self.showNormal()
        else:
            self.showFullScreen()
        self._fs = not self._fs
            
    def start(self):
        self._timer.start(self._interval)

    def stop(self):
        self._timer.stop()

    def togglePaused(self):
        if self._timer.isActive():
            self.stop()
        else:
            self.start()

    def mousePressEvent(self,event):
        super(DisplayWidget, self).mousePressEvent(event)
        if event.button() == c.Qt.LeftButton:
            self._mouse_moving = 0
        elif event.button() == c.Qt.MidButton:
            self._mouse_moving = 1
        elif event.button() == c.Qt.RightButton:
            self._mouse_moving = 2
        self._mouse_x = event.x()
        self._mouse_y = event.y()
        event.accept()
        
    def mouseMoveEvent(self, event):
        super(DisplayWidget, self).mouseMoveEvent(event)
        if self._trace != -1 and self._trace_v:
            event.accept()
            return
        if self._mouse_moving == -1:
            event.accept()
            return
        elif self._mouse_moving == 0:
            self._phi = - (event.x() - self._mouse_x) / 10.0 + self._phi
            new_theta  = - (event.y() - self._mouse_y) / 10.0 + self._theta
            if new_theta <=180 and new_theta >= 0:
                self._theta = new_theta
            self._updateCamera()
        elif self._mouse_moving == 2:
            self._x = (event.x() - self._mouse_x) / 800.0 + self._x
            self._y = - (event.y() - self._mouse_y) / 800.0 + self._y
            self._updateCamera()
        self._mouse_x = event.x()
        self._mouse_y = event.y()
        event.accept()
        
    def mouseReleaseEvent(self, event):
        super(DisplayWidget, self).mouseReleaseEvent(event)
        if self._mouse_moving == 1:
            self._reset_view()
        self._mouse_moving = -1
        event.accept()
        
    def wheelEvent(self,event):
        step = event.delta() / 100.0
        if self._view_angle <= 10 and not event.modifiers() == c.Qt.ControlModifier:
            step = step > 0 and self._view_angle / 20.0 or -self._view_angle / 10.0
        if self._view_angle - step < 0 or self._view_angle - step > 180:
            return
        self._view_angle = self._view_angle - step
        self._updateCamera()
        event.accept()
        
    def _get_angle_by_v(self, v):
        phi = 180 + math.degrees(math.atan2(v.y , v.x))
        theta = 180 - math.degrees(math.atan2(math.sqrt(v.x**2 + v.y**2) ,v.z)) 
        return phi, theta

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        _array = galaxy.\
                celaArray_frompointer(self._galaxy.\
                                      output())
        if self._trace >= 0:
            self._dx = _array[self._trace].p.x * self._scale_factor
            self._dy = _array[self._trace].p.y * self._scale_factor
            self._dz = _array[self._trace].p.z * self._scale_factor
            if self._trace_v:
                self._phi, self._theta = self._get_angle_by_v(_array[self._trace].v)
            self.setCamera()
            
        gl.glColor(*self._planec)
        step = self._planes / float(self._celld)
        gl.glBegin(gl.GL_LINES)
        for i in xrange(2 * self._celld):
            gl.glVertex(- self._planes + i*step,
                        - self._planes)
            gl.glVertex(- self._planes + i*step,
                        self._planes - step)
        for i in xrange(2 * self._celld):
            gl.glVertex(- self._planes,
                        - self._planes + i*step)
            gl.glVertex(self._planes - step,
                        - self._planes + i*step)

        gl.glEnd()
        if self._axisl > 0:
            gl.glColor(*self._axisc)
            gl.glBegin(gl.GL_LINES)
            gl.glVertex(0,0,0)
            gl.glVertex((self._axisl+1) * step, 0 ,0)
            gl.glEnd()
            gl.glPushMatrix()
            gl.glTranslate(self._axisl * step, 0, 0)
            gl.glRotate(90, 0, 1, 0)
            glut.glutWireCone(step / 4, step , 8, 8)
            gl.glPopMatrix()

            gl.glBegin(gl.GL_LINES)
            gl.glVertex(0,0,0)
            gl.glVertex(0,(self._axisl+1) * step, 0)
            gl.glEnd()
            gl.glPushMatrix()
            gl.glTranslate(0, self._axisl * step, 0)
            gl.glRotate(-90, 1, 0, 0)
            glut.glutWireCone(step / 4, step , 8, 8)
            gl.glPopMatrix()

            gl.glBegin(gl.GL_LINES)
            gl.glVertex(0,0,0)
            gl.glVertex(0,0,(self._axisl+1) * step)
            gl.glEnd()
            gl.glPushMatrix()
            gl.glTranslate(0,0,self._axisl * step)
            glut.glutWireCone(step / 4, step , 8, 8)
            gl.glPopMatrix()

        for i in xrange(self._n):
            graphic = self._graphic[i]

            if "color" in graphic:
                gl.glColor(*graphic["color"])
            else:
                gl.glColor(*self._planec)

            if "style" in graphic:
                style = graphic["style"]
            else:
                style = self._dstyle
                
            if style == "solid":
                drawfunc = glut.glutSolidSphere
            else:
                drawfunc = glut.glutWireSphere
                
            gl.glPushMatrix()
            gl.glTranslate(_array[i].p.x,
                           _array[i].p.y,
                           _array[i].p.z)
            drawfunc(graphic["radius"], 16, 16)
            if i == self._trace:
                gl.glColor(0.0,1.0,0.0)
                
                gl.glScale(graphic["radius"],graphic["radius"],graphic["radius"])
                gl.glTranslate(0 ,0, 3)
                glut.glutSolidOctahedron()
                gl.glColor(1.0,1.0,1.0) 
                glut.glutWireOctahedron()
            gl.glPopMatrix()
            if self._trace_line and (self._trace == i or self._trace == - 1 ) :
                if self._timer.isActive():
                    self._trace_buffer[i].append(_array[i].p.x)
                    self._trace_buffer[i].append(_array[i].p.y)
                    self._trace_buffer[i].append(_array[i].p.z)
                    if len(self._trace_buffer[i]) > self._trace_buffer_size:
                        self._trace_buffer[i].pop(0)
                        self._trace_buffer[i].pop(0)
                        self._trace_buffer[i].pop(0)
                gl.glBegin(gl.GL_LINE_STRIP)
                line_step = 3 * self._line_int
                num = len(self._trace_buffer[i]) / line_step
                for j in xrange(num):
                    if self._shadow:
                        color = [float(k) / num * j for k in self._axisc]
                    else:
                        color = self._axisc
                    gl.glColor(*color)
                    gl.glVertex(self._trace_buffer[i][j * line_step],
                                self._trace_buffer[i][j * line_step+ 1],
                                self._trace_buffer[i][j * line_step+ 2])
                gl.glEnd()
            
    def setTraceCela(self,celaN):
        if celaN < -1 or celaN >= self._n :
            raise ValueError
        self._trace = celaN
        self._vDisplay.setTrace(celaN)

    def initializeGL(self):
        glut.glutInit([])
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthMask(True)
        gl.glDepthFunc(gl.GL_LEQUAL)
        gl.glDepthRange(0.0,1.0)
        gl.glClearColor(0,0,0,0)
        gl.glClearDepth(1.0)
        gl.glShadeModel(gl.GL_SMOOTH)
        if self._light:
            gl.glLight(gl.GL_LIGHT0, gl.GL_AMBIENT, [0.9,0.9,0.9,1])
            gl.glLight(gl.GL_LIGHT0, gl.GL_DIFFUSE, [1,1,1,1])
            gl.glLight(gl.GL_LIGHT0, gl.GL_SPECULAR, [1,1,1,1])
            gl.glLight(gl.GL_LIGHT0, gl.GL_POSITION, [1,1,0,0])
            gl.glEnable(gl.GL_NORMALIZE)
            gl.glEnable(gl.GL_LIGHTING)
            gl.glEnable(gl.GL_LIGHT0)
            gl.glEnable(gl.GL_COLOR_MATERIAL)
            gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)
            gl.glMaterial(gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR, [1,1,1,1])
            gl.glMaterial(gl.GL_FRONT_AND_BACK, gl.GL_EMISSION, [0,0,0,1])
            gl.glMaterial(gl.GL_FRONT_AND_BACK, gl.GL_SHININESS, 10)
        gl.glLineWidth(self._linew)
        if self._multisample:
            gl.glEnable(gl.GL_MULTISAMPLE)
        if self._smooth == 1:
            gl.glEnable(gl.GL_POINT_SMOOTH)
            gl.glEnable(gl.GL_LINE_SMOOTH)
            gl.glEnable(gl.GL_POLYGON_SMOOTH)
            gl.glHint(gl.GL_POINT_SMOOTH_HINT, gl.GL_FASTEST)
            gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_FASTEST)
            gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_FASTEST)
        if self._smooth == 2:
            gl.glEnable(gl.GL_POINT_SMOOTH)
            gl.glEnable(gl.GL_LINE_SMOOTH)
            gl.glEnable(gl.GL_POLYGON_SMOOTH)
            gl.glHint(gl.GL_POINT_SMOOTH_HINT, gl.GL_NICEST)
            gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)
            gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST)

    def setCamera(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(self._view_angle, self._aspect, 1e-2, 100)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glTranslate(self._x, self._y, 0)
        glu.gluLookAt(self._rho * math.sin(math.radians(self._theta)) * math.cos(math.radians(self._phi)) + self._dx,
                      self._rho * math.sin(math.radians(self._theta)) * math.sin(math.radians(self._phi)) + self._dy,
                      self._rho * math.cos(math.radians(self._theta)) + self._dz,
                      self._dx, self._dy, self._dz,
                      0, 0, 1)
        gl.glScale(self._scale_factor,
                   self._scale_factor,
                   self._scale_factor)

        
    def resizeGL(self, w, h):
        gl.glViewport(0, 0, w, h)
        self._aspect = float(w)/float(h)
        self.setCamera()

        
