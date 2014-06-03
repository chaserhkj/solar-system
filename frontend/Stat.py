#!/usr/bin/env python2
# Copyright (C) 2013-2014 Kangjing Huang & Zhiyi Xu
# For further infomation, see LICENSE.txt

import json,sys,math

def main():
    if len(sys.argv) < 2:
        print "Usage : %s <Filename to read from>"%sys.argv[0]
        sys.exit(0)
    filename = sys.argv[1]

    with open(filename) as f:
        data = json.load(f)["celas"]
    cords = [i["position"] for i in data]
    mid_point = map(lambda x: sum(x) / len(x), zip(*cords))
    Rs = [math.sqrt((i[0] - mid_point[0])**2 +
                    (i[1] - mid_point[1])**2 +
                    (i[2] - mid_point[2])**2)
          for i in cords]
    Rs.sort()
    print "\n".join(map(str,Rs))
    

if __name__=="__main__":
    main()
        
