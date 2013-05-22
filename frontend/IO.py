#!/usr/bin/env python2
import json
import system

class SystemIO(object):
    def __init__(self):
        self.celas = None
        self.N = 0

    def load(self, filename):
        with file(filename, "r") as f:
            data=json.load(f)
            
        self.N = len(data)    
        self.celas = system.celaArray(self.N)
        for i in xrange(self.N):
            p = system.vector(data[i]["position"][0],
                              data[i]["position"][1],
                              data[i]["position"][2])
            v = system.vector(data[i]["velocity"][0],
                              data[i]["velocity"][1],
                              data[i]["velocity"][2])
            self.celas[i] = system.cela(data[i]["id"], p, v,
                                        data[i]["mass"],
                                        data[i]["name"])

    def save(self, filename):
        with file(filename, "w") as f:
            json.dump(self.get_data(), f, indent=2)
            
    def get_data(self):
        data_list = []
        for i in xrange(self.N):
            data = {"id": self.celas[i].id,
                    "position": [self.celas[i].p.x,
                                 self.celas[i].p.y,
                                 self.celas[i].p.z],
                    "velocity": [self.celas[i].v.x,
                                 self.celas[i].v.y,
                                 self.celas[i].v.z],
                    "mass": self.celas[i].m,
                    "name": self.celas[i].name
                }
            data_list.append(data)
        return data_list
            
    def get_array(self):
        return self.celas
