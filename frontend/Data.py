#!/usr/bin/env python2
import json
import system

class SystemData(object):
    def __init__(self):
        self.celas = []

    def load(self, filename):
        self.celas = []
        with file(filename, "r") as f:
            data=json.load(f)
            
        for i in data:
            p = system.vector(i["position"][0],
                              i["position"][1],
                              i["position"][2])
            v = system.vector(i["velocity"][0],
                              i["velocity"][1],
                              i["velocity"][2])
            self.celas.append(system.cela(i["id"], p, v,
                                          i["mass"], i["name"]))

    def save(self, filename):
        with file(filename, "w") as f:
            json.dump(self.get_data(), f, indent=2)
            
    def get_data(self):
        data_list = []
        for i in self.celas:
            data = {"id": i.id,
                    "position": [i.p.x, i.p.y, i.p.z],
                    "velocity": [i.v.x, i.v.y, i.v.z],
                    "mass": i.m,
                    "name": i.name
                }
            data_list.append(data)
        return data_list
            
    def get_array(self):
        array = system.celaArray(len(self.celas))
        for i in xrange(len(self.celas)):
            array[i] = self.celas[i]
        return array
