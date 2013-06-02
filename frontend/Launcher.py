#!/usr/bin/env python2
import sys
import PyQt4.QtGui as g
import galaxy
import Display
import IO

if __name__ == '__main__':
    app = g.QApplication(sys.argv)
    font = g.QFont()
    font.setPointSize(10)
    app.setFont(font)
    io = IO.RuntimeIO()
    filename = g.QFileDialog.getOpenFileName()
    if not filename:
        sys.exit(1)
    try:
        io.load(filename)
    except Exception as e:
        g.QMessageBox.critical(None, "I/O error","Load exception %s: %s"%(e.__class__.__name__, e))
        sys.exit(1)
    obj = galaxy.galaxy(
        n = io.N,
        stars = io.celas,
        step = io.global_settings["Calculation step"],
        G = io.global_settings["Gravity constant"],
        t = io.global_settings["Initial time"],
        r = io.global_settings["Recursion depth"],
        o = io.global_settings["Recursive coefficient"],
        numt = io.global_settings["Thread count"],
        aplfx = io.global_settings["Fix applied"]
    )
    display = Display.DisplayWidget(
        galaxy_obj = obj,
        graphic_obj = io.graphic,
        scale = io.global_settings["Drawing scale"],
        step_count = io.global_settings["Step per frame"],
        interval = io.global_settings["Frame interval"],
        plane_scale = io.global_settings["Plane scale"],
        plane_color = io.global_settings["Plane color"],
        cell_density = io.global_settings["Plane cell density"],
        axis_length = io.global_settings["Axis length"],
        axis_color = io.global_settings["Axis color"],
        trace_buffer = io.global_settings["Trace buffer size"],
        shadow_line = io.global_settings["Show shadow line"],
        line_interval = io.global_settings["Line drawing interval"],
        line_width = io.global_settings["Line width"],
        light = io.global_settings["Enable lighting"],
        default_style = io.global_settings["Default sphere style"],
        smooth = io.global_settings["Enable smooth"],
        multisampling = io.global_settings["Enable multi-sampling"]
    )
    saveB = g.QPushButton("Save current state to file",display)
    saveB.setGeometry(0,200,200,30)
    def save():
        display.stop()
        save_io = IO.RuntimeIO()
        save_io.celas = display.getCelas()
        save_io.graphic = io.graphic
        io.global_settings["Initial time"] = display.getTime()
        save_io.global_settings = io.global_settings
        save_io.N = display.getCelaNum()
        filename = g.QFileDialog.getSaveFileName()
        if filename:
            save_io.save(filename)
    saveB.clicked.connect(save)
    display.show()
    sys.exit(app.exec_())
