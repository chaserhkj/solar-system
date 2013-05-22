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

vpath %.cpp backend
vpath %.h backend


dist: backend/galaxy.py backend/_galaxy.so
	$(MKDIR) dist
	$(CP) frontend/*.py dist
	$(CP) backend/_galaxy.so backend/galaxy.py dist

$(BACKEND_OBJS): %.o : %.cpp %.h
	$(CXX) $(CXXFLAGS) $< -o $@

backend/galaxy.py: interface.cpp

backend/_galaxy.so: interface.o $(BACKEND_OBJS)
	$(LD) $(LFLAGS) $< -o backend/_galaxy.so

interface.cpp: backend/interface.i
	$(SWIG) $(SWIGFLAGS) -o backend/interface.cpp backend/interface.i 

interface.o: interface.cpp $(INTERFACE_H)
	$(CXX) $(CXXFLAGS) $(PYTHON_INCLUDE) backend/interface.cpp -o $@


.PHONY: clean
clean:
	$(RM) dist
	$(RM) *.o backend/interface.cpp
	$(RM) backend/galaxy.py backend/_galaxy.so
