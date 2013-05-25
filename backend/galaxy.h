#ifndef GALAXY_H
#define GALAXY_H

#include <string>
#include "vector.h"

using std::string;

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
    cela() {}

    void newp1(double dt); //Calculate new p1
    void flush(double dt); //Flush p1 back to p and culculate new v
};

class galaxy
{
private:
    cela* celas; // array of celas
    int n; //number of celas;
    double dt; //Time step
    double G; // Gravity constant
    double ek; // System Kinetic energy
    double ep; // System Potential energy
    double e00; // System initial total energy
    double e0; // System fixed total energy
    double t; // Physical time

    int recurdepth; // Recursion depth
    double omega; // Recursive coefficient [0,1]
    bool applyenergyfix;

    int num_threads; // Used for OpenMP

    void setacc(); // Set accelration for celas[i] based on p 
    void setcollision(); // Set collision flag 
    void setacc1(); // Get accelration for celas[i] based on p1

    void calculateEnergy(); // Calculate system energy

public:
    galaxy(int n, cela* stars, double step=1, double G=1, double t=0, int r=0,
            double o=0.5, int numt=0 /*Default: = processors*/, bool
            aplfx=false);
    ~galaxy(); 

    void setGravity(double gc);
    void setTimeStep(double step);
    bool togglefix(); // Retrun status after toggle
    void fixenergyto0(); // Fix system energy to initial status
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


#endif //GALAXY_H
