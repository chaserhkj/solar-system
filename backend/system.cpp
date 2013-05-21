#include <cmath>
#include "system.h"

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

void cela::run(vector force, double dt) 
{
    p = p + v * dt + force / m * dt * dt / 2;
    v = v + force/m * dt;
}

CelaSystem::CelaSystem(int n, cela* stars, double step, double gc):dt(step), G(gc)
{
    celas = new cela[n];
    int i;
    for (i=0;i<n;i++) {
        celas[i] = stars[i];
    }
}

void CelaSystem::setGravity(double gc)
{
    G = gc;
}

void CelaSystem::setTimeStep(double step)
{
    dt = step;
}

int CelaSystem::getCelaNum()
{
    return n;
}

cela* CelaSystem::output(){
    return celas;
}

void CelaSystem::run() {
    int i,j;
    vector force;
    vector d; //distance
    for (i=0;i<n;i++) {
        force = vector(0,0,0);
        for (j=0;j<n;j++) { // cela[j]'s gravity on cela[i]
            if (j != i) { //Not myself
                d = celas[j].p - celas[i].p;
                force = force + G * celas[i].m * celas[j].m * d / (d.mag() * d.mag() *
                        d.mag());
            }
        }
        celas[i].run(force,dt);
    }
}
                




        



    
