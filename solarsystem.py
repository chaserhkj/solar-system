import json
globalvariables={
    "Calculation step":0.01,
    "Gravity constant":1,
    "Initial time":0,
    "Recursion depth":69,
    "Recursive coefficient":0.01,
    "Thread count":1,
    "Fix applied":False,
    "Drawing scale":30000,
    "Step per frame":10,
    "Frame interval":20,
    "Plane color":[0.6,0.8,1.0],
    "Plane scale":50000,
    "Plane cell density":20,
    "Axis length":20,
    "Axis color":[1,1,1],
    "Line width":1,
    "Default sphere style":"wire",
    "Trace buffer size":500,
    "Show shadow line":True,
    "Line drawing interval":1,
    "Enable lighting":True,
    "Enable smooth":2,
    "Enable multi-sampling":True,
    "Start system at startup":False
    }

planets=[]
Sunstyle={"radius":240,"color":[1,0,0]}
planets.append({"name":"Sun","position":[0,0,0],"velocity":[0,0,0],"mass":1000000,"radius":20,"graphic":Sunstyle})

Mercurystyle={"radius":3.8,"color":[1,1,1]}
planets.append({"name":"Mercury","position":[390,0,0],"velocity":[0,20,0],"mass":0.0553,"radius":3.8,"graphic":Mercurystyle})

Venusstyle={"radius":9.49,"color":[1,1,1]}
planets.append({"name":"Venus","position":[720,0,0],"velocity":[0,20,0],"mass":0.815,"radius":9.49,"graphic":Venusstyle})

Earthstyle={"radius":10,"color":[0.6,0.8,1]}
planets.append({"name":"Earth","position":[1000,0,0],"velocity":[0,20,0],"mass":1,"radius":10,"graphic":Earthstyle})

Marsstyle={"radius":5.32,"color":[0,1,1]}
planets.append({"name":"Mars","position":[1520,0,0],"velocity":[0,20,0],"mass":0.1074,"radius":5.32,"graphic":Marsstyle})

Jupiterstyle={"radius":112,"color":[0,1,1]}
planets.append({"name":"Jupiter","position":[5200,0,0],"velocity":[0,20,0],"mass":317.834,"radius":112,"graphic":Jupiterstyle})

Saturnstyle={"radius":94.1,"color":[0,1,1]}
planets.append({"name":"Saturn","position":[9540,0,0],"velocity":[0,20,0],"mass":95.159,"radius":94.1,"graphic":Saturnstyle})

Uranusstyle={"radius":40.6,"color":[0,1,1]}
planets.append({"name":"Uranus","position":[19200,0,0],"velocity":[0,20,0],"mass":14.5,"radius":40.6,"graphic":Uranusstyle})

Neptunestyle={"radius":38.8,"color":[0,1,1]}
planets.append({"name":"Neptune","position":[30100,0,0],"velocity":[0,20,0],"mass":17.2,"radius":38.8,"graphic":Neptunestyle})

solar={"global":globalvariables,"celas":planets}

with open("solarsystem.json","w") as f:
    json.dump(solar,f,indent=2)

