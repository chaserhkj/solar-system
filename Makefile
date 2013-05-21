CXX = g++ -c
CFLAGS = $(CFLAGS) -fpic -Wall -Wextra
CXXFLAGS = $(CFLAGS)
PYTHON_INCLUDE = -I/usr/include/python2.7
LD = g++
LFLAGS = $(LFLAGS) -fpic -shared
SWIG = swig -python -c++
SWIGFLAGS = -Wall
RM = rm -rf
CP = cp -r
MKDIR = mkdir -p

dist: backend/system.py backend/_system.so
	$(MKDIR) dist
	$(CP) frontend/*.py dist
	$(CP) backend/_system.so backend/system.py dist

system.o: backend/system.cpp backend/system.h
	$(CXX) $(CXXFLAGS) backend/system.cpp

backend/system.py: backend/system_wrap.cpp

backend/system_wrap.cpp: backend/system.h backend/system.i
	$(SWIG) $(SWIGFLAGS) -o backend/system_wrap.cpp backend/system.i 

system_wrap.o: backend/system_wrap.cpp
	$(CXX) $(CXXFLAGS) $(PYTHON_INCLUDE) backend/system_wrap.cpp

backend/_system.so: system_wrap.o system.o
	$(LD) $(LFLAGS) system_wrap.o system.o -o backend/_system.so

clean:
	$(RM) dist
	$(RM) *.o backend/system_wrap.cpp
	$(RM) backend/system.py backend/_system.so
