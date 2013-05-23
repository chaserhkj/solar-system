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
    double r; //Radius
    bool c; //Collision flag
    vector p; //Position
    vector p1; //Position used for recursive calculation
    vector v; //Velocity
    vector a; //Acceleration

    cela(int id, vector p, vector v, double m, double r, string name=""):
        id(id),name(name),m(m),r(r),p(p),v(v) {}
    cela() {}
};

class galaxy
{
public:
    galaxy(int n, cela* stars, double step=1, double G=1, double t=0, int recdpt=0, bool aplfx=false);
    ~galaxy(); 

    void setGravity(double gc);
    void setTimeStep(double step);
    void run();
    int getCelaNum();
    double getTime(); //Get Physical time
    double getEnergy(); // Get system total energy
    cela* output();
};

%include "carrays.i"
%array_class(cela, celaArray);
