# Copyright (C) 2013 Kangjing Huang & Zhiyi Xu
# For further infomation, see LICENSE.txt
CXX := g++ -c
CFLAGS := $(CFLAGS) -fpic -fopenmp -Wall -Wextra
CXXFLAGS := $(CFLAGS)
BACKEND_INCLUDE := -I./backend/
PYTHON_INCLUDE := -I/usr/include/python2.7
INTERFACE_INCLUDE := $(PYTHON_INCLUDE) $(BACKEND_INCLUDE)
LD := g++
LFLAGS := $(LFLAGS) -fopenmp -fpic -shared
SWIG := swig -python -c++
SWIGFLAGS := -Wall -keyword
RM := rm -rf
CP := cp -r
MKDIR := mkdir -p

BACKEND_OBJS := vector.o galaxy.o
INTERFACE_H := vector.h galaxy.h

BACKEND_DIST := galaxy.py _galaxy.so
FRONTEND_DIST := IO.py Editor.py Display.py Launcher.py

vpath %.cpp backend
vpath %.h backend
vpath %.py frontend

.PHONY: clean

all: dist

dist: $(BACKEND_DIST) $(FRONTEND_DIST)
	$(MKDIR) dist
	$(CP) $? dist

$(BACKEND_OBJS): %.o : %.cpp %.h
	$(CXX) $(CXXFLAGS) $< -o $@

galaxy.py: interface.cpp

_galaxy.so: interface.o $(BACKEND_OBJS)
	$(LD) $(LFLAGS) $^ -o _galaxy.so

interface.cpp: backend/interface.i
	$(SWIG) $(SWIGFLAGS) -o $@ $<

interface.o: interface.cpp $(INTERFACE_H)
	$(CXX) $(CXXFLAGS) $(INTERFACE_INCLUDE) $< -o $@

clean:
	$(RM) dist
	$(RM) *.o interface.cpp
	$(RM) galaxy.py _galaxy.so
