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
    vector * sps; // Scaled positions
    int n; //number of celas;
    double dt; //Time step
    double G; // Gravity constant
    double ek; // System Kinetic energy
    double ep; // System Potential energy
    double e0; // System initial total energy

    double coscl; // Coordination scale

    int recurdepth; // Recursion depth
    bool applyenergyfix;

    vector getacc(int i); // Get accelration for celas[i] based on p
    vector getacc1(int i); // Get accelration for celas[i] based on p1

    void calculateEnergy(); // Calculate system energy

public:
    galaxy(int n, cela* stars, double step=1, double G=1, double coscl=1, int recdpt=0, bool aplfx=false);
    ~galaxy(); 

    void setGravity(double gc);
    void setTimeStep(double step);
    void run();
    int getCelaNum();
    double getEnergy(); // Get system total energy
    vector* getScaledPositions();
    cela* output();
};


#endif //GALAXY_H
