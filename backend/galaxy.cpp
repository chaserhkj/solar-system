#include <cmath>
#include "galaxy.h"

vector vector::operator+ (const vector &v) const
{
    return vector(x+v.x, y+v.y, z+v.z);
}

vector vector::operator- (const vector &v) const
{
    return vector(x-v.x,y-v.y,z-v.z);
}

vector vector::operator* (double s) const
{
    return vector(x*s, y*s, z*s);
}

double vector::operator* (const vector &v) const
{
    return x*v.x+y*v.y+z*v.z;
}

vector vector::operator/ (double s) const
{
    return vector(x/s, y/s, z/s);
}

double vector::mag() const
{
    return sqrt(x*x+y*y+z*z);
}

vector operator* (double s, const vector &v)
{
    return vector(v.x*s, v.y*s, v.z*s);
}

void cela::ptop1()
{
    p1 = p;
}

void cela::newp1(double dt)
{
    p1 = p + v * dt + a * dt * dt / 2;
}

void cela::flush() 
{
    v = v + a * dt;
    p = p1;
}

galaxy::galaxy(int n, cela* stars, double step, double G):dt(step), G(G)
{
    celas = new cela[n];
    int i;
    for (i=0;i<n;i++) {
        celas[i] = stars[i];
    }
}

void galaxy::setGravity(double gc)
{
    G = gc;
}

void galaxy::setTimeStep(double step)
{
    dt = step;
}

int galaxy::getCelaNum()
{
    return n;
}

cela* galaxy::output(){
    return celas;
}

void galaxy::run(int recurdepth) {
    int i,j,r;
    vector acc; //acceleration
    vector d; //distance
    for (i=0;i<n;i++) {
        celas[i].ptop1();
    }
    for (i=0;i<n;i++) {
        acc = vector(0,0,0);
        for (j=0;j<n;j++) { // cela[j]'s gravity on cela[i]
            if (j != i) { //Not myself
                d = celas[j].p1 - celas[i].p1;
                acc = acc + G * celas[j].m * d / (d.mag() * d.mag() *
                        d.mag());
            }
        }
        celas[i].a = acc;
    }
    for (r=0;r<recurdepth;i++) {
        for (i=0;i<n;i++) {
            celas[i].newp1(dt);
        }
        for (i=0;i<n;i++) {
            acc = vector(0,0,0);
            for (j=0;j<n;j++) { // cela[j]'s gravity on cela[i]
                if (j != i) { //Not myself
                    d = celas[j].p1 - celas[i].p1;
                    acc = acc + G * celas[j].m * d / (d.mag() * d.mag() *
                            d.mag());
                }
            }
            celas[i].a = (celas[i].a + acc) / 2;
        }
    }
    for (i=0;i<n;i++) {
        celas[i].flush();
    }
}
                




        



    
