#include <cmath>
#include "galaxy.h"

void cela::newp1(double dt)
{
    p1 = p + v * dt + a * dt * dt / 2;
}

void cela::flush(double dt) 
{
    v += a * dt;
    p = p1;
}

galaxy::galaxy(int n, cela* stars, double step, double G, int
        recdpt, bool aplfx):n(n), dt(step), G(G), recurdepth(recdpt), applyenergyfix(aplfx)
{
    celas = new cela[n];
    int i;
    for (i=0;i<n;i++) {
        celas[i] = stars[i];
    }

    this->calculateEnergy();
    e0 = ek + ep;
}

galaxy::~galaxy()
{
    delete [] celas;
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

vector galaxy::getacc(int i)
{
    int j;
    vector r; //vector distance
    double d; //distance
    vector acc(0,0,0);

    for (j=0;j<n;j++) { // cela[j]'s gravity on cela[i]
        if (j != i) { //Not myself
            r = celas[j].p - celas[i].p;
            d = r.mag();
            if (d < (celas[i].r + celas[j].r)) {  //Collision
                return 0;            
            } else {
                acc += G * celas[j].m * r / (d * d * d);
            }
        }
    }

    return acc;
}


vector galaxy::getacc1(int i)
{
    int j;
    vector r; //vector distance
    double d; //distance
    vector acc(0,0,0);

    for (j=0;j<n;j++) { // cela[j]'s gravity on cela[i]
        if (j != i) { //Not myself
            r = celas[j].p1 - celas[i].p1;
            d = r.mag();
            acc += G * celas[j].m * r / (d * d * d);
        }
    }

    return acc;
}

void galaxy::calculateEnergy() 
{
    int i,j;
    ek = 0;
    ep = 0;
    for (i=0;i<n;i++) {
        ek += celas[i].m * (celas[i].v * celas[i].v) / 2;
        for (j=0;j<i;j++) {
            ep -= G * celas[i].m * celas[j].m / (celas[j].p - celas[i].p).mag();
        }
    }
}

double galaxy::getEnergy()
{
    if (applyenergyfix) {
        return e0;
    }

    this->calculateEnergy();
    return ek + ep;
}

void galaxy::run()
{
    int i,rec;
    double co; // fix coefficient

    for (i=0;i<n;i++) {
        celas[i].a = getacc(i);
    }

    for (rec=0;rec<recurdepth;rec++) { //Recursive calculation
        for (i=0;i<n;i++) {
            celas[i].newp1(dt);
        }
        for (i=0;i<n;i++) {
            celas[i].a = (celas[i].a + getacc1(i)) / 2;
        }
    }

    for (i=0;i<n;i++) { //Flush back
        celas[i].newp1(dt);
        celas[i].flush(dt);
    }

    if (applyenergyfix) {  // Fix system energy
        this->calculateEnergy();
        co = sqrt((e0 - ep) / ek);
        for (i=0;i<n;i++) {
            celas[i].v *= co;
        }
    }
}
