%module galaxy
%{
#include "vector.h"
#include "galaxy.h"
%}

%include "std_string.i"

using std::string;

class vector //3-D
{
public:
    double x,y,z;

    vector(double x=0, double y=0, double z=0):x(x),y(y),z(z) {}

    
};

class cela //celestial body
{
public:
    int id; //Equals subscript
    string name; //Optional
    double m; //Mass
    double r; //Radius
    bool c; //Collision flag
    vector p; //Position
    vector p1; //Position used for recursive calculation
    vector v; //Velocity
    vector a; //Acceleration

    cela(int id, vector p, vector v, double m, double r, string name=""):
        id(id),name(name),m(m),r(r),p(p),v(v) {}
};

class galaxy
{
public:
    galaxy(int n, cela* stars, double step=1, double G=1, double t=0, int r=0,
            double o=0.5, int numt=-1 /*Default: = processors*/, bool
            aplfx=false);
    ~galaxy(); 

    void setGravity(double gc);
    void setTimeStep(double step);
    bool togglefix(); // Retrun status after toggle
    void setThreads(int numt=0); // Set number of threads;

    void run();

    int getCelaNum();
    double getTime(); //Get Physical time
    double getEnergy(); // Get system total energy
    int getRecDpt();
    double getOmega();
    double getG();
    double getStep();
    int getThreads(); // Get number of threads;
    bool appliedfix(); // True if applied energy fix

    cela* output();
};

%include "carrays.i"
%array_class(cela, celaArray);
