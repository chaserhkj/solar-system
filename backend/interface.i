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

    vector operator+ (const vector &v) const; 
    void operator+= (const vector &v);

    vector operator- (const vector &v) const;
    void operator-= (const vector &v);

    vector operator* (double s) const; //Dot scala
    void operator*= (double s);

    vector operator/ (double s) const;
    void operator/= (double s);

    double operator* (const vector &v) const; //Dot another vector

    bool operator== (const vector &v) const; //Comparison
    double mag() const; //magnitude
    
};

class cela //celestial body
{
public:
    int id; //Equals subscript
    string name; //Optional
    double m; //Mass
    vector p; //Position
    vector v; //Velocity

    cela(int id, vector p, vector v, double m, string name=""):
        id(id),name(name),m(m),p(p),v(v) {}
    cela() {}

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
    void calculateEnergy(); // Calculate system energy
    cela* output();
};



%include "carrays.i"
%array_class(cela, celaArray);
