import json
globalvariables={
    "Calculation step":0.01,
    "Gravity constant":1,
    "Initial time":0,
    "Recursion depth":69,
    "Recursive coefficient":0.01,
    "Thread count":1,
    "Fix applied":False,
    "Drawing scale":1000,
    "Step per frame":10,
    "Frame interval":20,
    "Plane color":[0.6,0.8,1.0],
    "Plane scale":1000,
    "Plane cell density":20,
    "Axis length":20,
    "Axis color":[1,1,1],
    "Line width":1,
    "Default sphere style":"wire",
    "Trace buffer size":2000,
    "Show shadow line":True,
    "Line drawing interval":2,
    "Enable lighting":True,
    "Enable smooth":2,
    "Enable multi-sampling":True,
    "Start system at startup":False
    }

planets=[]
Sunstyle={"radius":20,"color":[1,0,0]}
planets.append({"name":"Sun","position":[0,0,0],"velocity":[0,0,0],"mass":1000000,"radius":20,"graphic":Sunstyle})
Mercurystyle={"radius":2,"color":[1,1,0]}
planets.append({"name":"Mercury","position":[80,0,0],"velocity":[0,20,0],"mass":1,"radius":20,"graphic":Mercurystyle})
solar={"global":globalvariables,"celas":planets}

with open("solarsystem.json","w") as f:
    json.dump(solar,f,indent=2)

