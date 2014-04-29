#/usr/bin/env python2
# Copyright (C) 2013-2014 Kangjing Huang & Zhiyi Xu
# For further infomation, see LICENSE.txt

import json,sys,random,copy

global_d = {
    "Trace buffer size": 1000, 
    "Plane cell density": 20, 
    "Gravity constant": 5.0, 
    "Enable smooth": 2, 
    "Line width": 1.0, 
    "Plane scale": 36000.0, 
    "Recursion depth": 69, 
    "Calculation step": 0.01, 
    "Enable multi-sampling": True, 
    "Frame interval": 20, 
    "Step per frame": 10, 
    "Line drawing interval": 1, 
    "Thread count": 1, 
    "Plane color": [
      0.6, 
      0.8, 
      1.0
    ], 
    "Drawing scale": 10000.0, 
    "Show shadow line": True, 
    "Axis color": [
      1.0, 
      1.0, 
      1.0
    ], 
    "Enable lighting": True, 
    "Start system at startup": False, 
    "Axis length": 20, 
    "Initial time": 0.0, 
    "Default sphere style": "wired", 
    "Fix applied": False, 
    "Recursive coefficient": 0.01
    }

template_cela_d = {
      "graphic": {
        "color": [
          1.0, 
          0.0, 
          0.0
        ], 
        "style": "wired", 
        "radius": 1.0
      }, 
      "name": "Cela", 
      "radius": 1.0, 
      "position": [
        0.0, 
        0.0, 
        0.0
      ], 
      "velocity": [
        0.0, 
        0.0, 
        0.0
      ], 
      "mass": 1.0
    }

x_range = 100.0
y_range = 100.0
z_range = 100.0


def main():
    if len(sys.argv) < 3:
        print "Usage : %s <Number of celas to generate> <Filename to save>"%sys.argv[0]
        sys.exit(0)
    n = int(sys.argv[1])
    filename = (sys.argv[2])
    celas = []
    for i in range(n):
        cela = copy.deepcopy(template_cela_d)
        cela["position"][0] = (random.random() - 0.5) * x_range
        cela["position"][1] = (random.random() - 0.5) * y_range
        cela["position"][2] = (random.random() - 0.5) * z_range
        celas.append(cela)
    with open(filename,"w") as f:
        json.dump({"global":global_d, "celas": celas}, f, indent = 1)


if __name__=="__main__":
    main()

