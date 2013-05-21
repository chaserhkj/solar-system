#ifndef GALAXY_H
#define GALAXY_H

#include <string>

using std::string;

class vector //3-D
{
public:
    double x,y,z;

    vector():x(0),y(0),z(0) {}
    vector(double x, double y, double z):x(x),y(y),z(z) {}

    vector operator+ (const vector &v) const; 
    vector operator- (const vector &v) const;
    vector operator* (double s) const; //Dot scala
    double operator* (const vector &v) const; //Dot another vector
    vector operator/ (double s) const;

    double mag() const; //magnitude
    

    //friend vector operator* (double s, vector v);
};

vector operator* (double s, const vector &v);

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

public:
    galaxy(int n, cela* stars, double step=1, double G=1);
    ~galaxy() {
        delete [] celas;
    }

    void setGravity(double gc);
    void setTimeStep(double step);
    void run(int recurdepth);
    int getCelaNum();
    cela* output();
};


#endif //GALAXY_H
