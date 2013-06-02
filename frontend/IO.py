#!/usr/bin/env python2
# Copyright (C) 2013 Kangjing Huang & Zhiyi Xu
# For further infomation, see LICENSE.txt
import json
try:
    import galaxy
    _no_runtime = False
except ImportError:
    _no_runtime = True
    
if not _no_runtime:
    class RuntimeIO(object):
        def __init__(self):
            self.celas = None
            self.graphic = None
            self.global_settings = None
            self.N = 0

        def load(self, filename):
            with file(filename, "r") as f:
                data = json.load(f)
                self.global_settings = data["global"]
                data = data["celas"]

            self.N = len(data)    
            self.celas = galaxy.celaArray(self.N)
            self.graphic = []
            for i in xrange(self.N):
                p = galaxy.vector(data[i]["position"][0],
                                  data[i]["position"][1],
                                  data[i]["position"][2])
                v = galaxy.vector(data[i]["velocity"][0],
                                  data[i]["velocity"][1],
                                  data[i]["velocity"][2])
                self.celas[i] = galaxy.cela(i, p, v,
                                            data[i]["mass"],
                                            data[i]["radius"],
                                            str(data[i]["name"]))
                self.graphic.append(data[i]["graphic"])

        def save(self, filename):
            data_list = []
            for i in xrange(self.N):
                data = {"position": [self.celas[i].p.x,
                                     self.celas[i].p.y,
                                     self.celas[i].p.z],
                        "velocity": [self.celas[i].v.x,
                                     self.celas[i].v.y,
                                     self.celas[i].v.z],
                        "radius": self.celas[i].r,
                        "mass": self.celas[i].m,
                        "name": self.celas[i].name,
                        "graphic": self.graphic[i]
                }
                data_list.append(data)

            with file(filename, "w") as f:
                json.dump({"global":self.global_settings, "celas":data_list}, f, indent=2)
                
class EdittimeIO(object):
    def __init__(self):
        self.data = {"celas":[],"global":{}}

    def load(self, filename):
        with file(filename, "r") as f:
            self.data=json.load(f)
            
    def save(self, filename):
        with file(filename, "w") as f:
            json.dump(self.data, f, indent=2)
            
