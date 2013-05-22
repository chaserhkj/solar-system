#include <cmath>
#include "galaxy.h"

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
    v += a * dt;
    p = p1;
}

galaxy::galaxy(int n, cela* stars, double step, double G):dt(step), G(G)
{
    celas = new cela[n];
    int i;
    for (i=0;i<n;i++) {
        celas[i] = stars[i];
    }

    this->calculateEnergy();
    e0 = ek + ep;
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

double galaxy::getEk()
{
    return ek;
}

double galaxy::getEp()
{
    return ep;
}

cela* galaxy::output(){
    return celas;
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


void galaxy::run(int recurdepth, bool applyfix)
{
    int i,j,rec;
    vector acc; //acceleration
    vector r; //vector distance
    double d; //distance
    double co; // fix coefficient

    if (applyfix) {  // Fix system energy
        co = sqrt((e0 - ep) / ek);
        for (i=0;i<n;i++) {
            celas[i].v *= co;
        }
    }

    for (i=0;i<n;i++) {
        acc = vector(0,0,0);
        for (j=0;j<n;j++) { // cela[j]'s gravity on cela[i]
            if (j != i) { //Not myself
                r = celas[j].p - celas[i].p;
                d = r.mag();
                acc += G * celas[j].m * r / (d * d * d);
            }
        }
        celas[i].a = acc;
    }

    for (rec=0;rec<recurdepth;rec++) { //Recursive calculation
        for (i=0;i<n;i++) {
            celas[i].newp1(dt);
        }
        for (i=0;i<n;i++) {
            acc = vector(0,0,0);
            for (j=0;j<n;j++) { // cela[j]'s gravity on cela[i]
                if (j != i) { //Not myself
                    r = celas[j].p1 - celas[i].p1;
                    d = r.mag();
                    acc += G * celas[j].m * r / (d * d * d);
                }
            }
            celas[i].a = (celas[i].a + acc) / 2;
        }
    }

    for (i=0;i<n;i++) { //Flush back
        celas[i].newp1();
        celas[i].flush();
    }
}
