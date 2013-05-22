CXX := g++ -c
CFLAGS := $(CFLAGS) -fpic -Wall -Wextra
CXXFLAGS := $(CFLAGS)
PYTHON_INCLUDE := -I/usr/include/python2.7
LD := g++
LFLAGS := $(LFLAGS) -fpic -shared
SWIG := swig -python -c++
SWIGFLAGS := -Wall
RM := rm -rf
CP := cp -r
MKDIR := mkdir -p

BACKEND_OBJS := vector.o galaxy.o
INTERFACE_H := vector.h galaxy.h

BACKEND_DIST := backend/galaxy.py backend/_galaxy.so
FRONTEND_DIST := IO.py Editor.py Display.py

vpath %.cpp backend
vpath %.h backend
vpath %.py frontend

.PHONY: clean dist

dist: $(BACKEND_DIST) $(FRONTEND_DIST)
	$(MKDIR) dist
	$(CP) $? dist

$(BACKEND_OBJS): %.o : %.cpp %.h
	$(CXX) $(CXXFLAGS) $< -o $@

backend/galaxy.py: interface.cpp

backend/_galaxy.so: interface.o $(BACKEND_OBJS)
	$(LD) $(LFLAGS) $^ -o backend/_galaxy.so

interface.cpp: backend/interface.i
	$(SWIG) $(SWIGFLAGS) -o backend/$@ $<

interface.o: interface.cpp $(INTERFACE_H)
	$(CXX) $(CXXFLAGS) $(PYTHON_INCLUDE) backend/$< -o $@

clean:
	$(RM) dist
	$(RM) *.o backend/interface.cpp
	$(RM) backend/galaxy.py backend/_galaxy.so
