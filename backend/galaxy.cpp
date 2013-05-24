#include <cmath>
#include <omp.h>
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

galaxy::galaxy(int n, cela* stars, double step, double G, double t, int
        r, double o, bool aplfx):n(n), dt(step), G(G), t(t), recurdepth(r), omega(o), applyenergyfix(aplfx)
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

bool galaxy::togglefix()
{
    if (applyenergyfix) {
        applyenergyfix = false;
    } else {
        applyenergyfix = true;
    }

    return applyenergyfix;
}

int galaxy::getCelaNum()
{
    return n;
}

double galaxy::getTime()
{
    return t;
}

int galaxy::getRecDpt()
{
    return recurdepth;
}

double galaxy::getOmega()
{
    return omega;
}

double galaxy::getG()
{
    return G;
}

double galaxy::getStep()
{
    return dt;
}

bool galaxy::appliedfix()
{
    return applyenergyfix;
}

cela* galaxy::output(){
    return celas;
}

void galaxy::setacc(int i)
{
    int j;
    vector r; //vector distance
    double d; //distance
    vector acc(0,0,0);
    vector epi; // unit vector in direction of p[j]-p[i]
    vector dvi,dvj;

    for (j=0;j<n;j++) { // cela[j]'s gravity on cela[i]
        if (j != i) { //Not myself
            r = celas[j].p - celas[i].p;
            d = r.mag();
            epi = r / d;
            if (d <= (celas[i].r + celas[j].r)) {  
                if (!celas[j].c && !celas[i].c) { //Collision with uncollided one
                celas[i].c = true;
                celas[j].c = true;
                dvj = 2 * celas[i].m / (celas[j].m + celas[i].m) * (celas[i].v - celas[j].v) * epi * epi;
                dvi = 2 * celas[j].m / (celas[j].m + celas[i].m) * (celas[j].v - celas[i].v) * epi * epi;
                celas[i].v += dvi;
                celas[j].v += dvj;
                }
                acc += G * celas[j].m * epi / ((celas[i].r + celas[j].r) * (celas[i].r + celas[j].r)); 
            } else {
                acc += G * celas[j].m * epi / (d * d);
            }
        }
    }

    celas[i].a = acc;
    return;
}


vector galaxy::getacc1(int i)
{
    int j;
    vector r; //vector distance
    double d; //distance
    vector acc(0,0,0);
    vector epi; // unit vector in direction of p[j]-p[i]

    if (celas[i].c) { //Collided in this step
        return celas[i].a;
    }

    for (j=0;j<n;j++) { // cela[j]'s gravity on cela[i]
        if (j != i) { //Not myself
            r = celas[j].p1 - celas[i].p1;
            d = r.mag();
            epi = r / d;
            if (d <= (celas[i].r + celas[j].r)) {  
                acc += G * celas[j].m * epi / ((celas[i].r + celas[j].r) * (celas[i].r + celas[j].r)); 
            } else {
                acc += G * celas[j].m * epi / (d * d);
            }
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
        celas[i].c = false;
    }

    for (i=0;i<n;i++) {
        setacc(i);
    }


    for (rec=0;rec<recurdepth;rec++) { //Recursive calculation
        for (i=0;i<n;i++) {
            celas[i].newp1(dt);
        }
        for (i=0;i<n;i++) {
            celas[i].a = celas[i].a * (1 - omega) + getacc1(i) * omega;
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

    t += dt;
}
