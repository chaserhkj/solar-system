%module galaxy
%{
#include "galaxy.h"
%}

%include "vector.i"
%include "std_string.i"

using std::string;

class cela //celestial body
{
public:
    int id; //Equals subscript
    string name; //Optional
    double m; //Mass
    vector p; //Position
    vector p1; //Position used for recursion
    vector v; //Velocity
    vector a; //Acceleration

    cela(int id, vector p, vector v, double m, string name=""):
        id(id),name(name),m(m),p(p),v(v) {}
    cela() {}

    void ptop1(); //Copy postion to p1
    void newp1(double dt); //Calculate new p1
    void flush(); //Flush p1 back to p and culculate new v
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
    double e0; // System initial total energy

public:
    galaxy(int n, cela* stars, double step=1, double G=1);
    ~galaxy() {
        delete [] celas;
    }

    void setGravity(double gc);
    void setTimeStep(double step);
    void run(int recurdepth=0, bool applyfix=false); //User needs to calculateEnergy() before applyfix
    int getCelaNum();
    double getEk();
    double getEp();
    double calculateEnergy(); // Calculate system energy
    cela* output();
};



%include "carrays.i"
%array_class(cela, celaArray);
