#include <cmath>
#include <omp.h>
#include "galaxy.h"

inline double max(double x1, double x2)
{
    return x1>x2?x1:x2;
}

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
        r, double o, int numt, bool aplfx):n(n), dt(step), G(G), t(t), recurdepth(r), omega(o), applyenergyfix(aplfx)
{
    if (numt == 0) { // Number of processors
        num_threads = omp_get_num_procs();
    } else {
        num_threads = numt;
    }
    omp_set_num_threads(num_threads);
    omp_set_nested(0); // Do not use nested parallel

    celas = new cela[n];
    int i;
#pragma omp parallel for
    for (i=0;i<n;i++) {
        celas[i] = stars[i];
    }

    this->calculateEnergy();
    e0 = ek + ep;
    e00 = e0;
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

void galaxy::fixenergyto0()
{
    int i;
    this->calculateEnergy();
    e0 = e00;
    double co = sqrt((e0 - ep) / ek);
#pragma omp parallel for
    for (i=0;i<n;i++) {
        celas[i].v *= co;
    }
}

bool galaxy::togglefix()
{
    if (applyenergyfix) {
        applyenergyfix = false;
    } else {
        this->calculateEnergy();
        e0 = ek + ep;
        applyenergyfix = true;
    }

    return applyenergyfix;
}

void galaxy::setThreads(int numt)
{
    if (numt == 0) {
        num_threads = omp_get_num_procs();
    } else {
        num_threads = numt;
    }
    omp_set_num_threads(num_threads);
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

int galaxy::getThreads()
{
    return num_threads;
}

bool galaxy::appliedfix()
{
    return applyenergyfix;
}

cela* galaxy::output(){
    return celas;
}

void galaxy::setacc()
{
    int i,j;
    vector r; //vector distance
    double d; //distance
    vector acc;

#pragma omp parallel for private(r,d,acc,j)
    for (i=0;i<n;i++) {
        acc.clear(); 
        for (j=0;j<n;j++) { // cela[j]'s gravity on cela[i]
            if (j != i) { //Not myself
                r = celas[j].p - celas[i].p;
                d = max(r.mag(), celas[j].r + celas[i].r);
                acc += G * celas[j].m * r / (r.mag() * d * d);
            }
        }
        celas[i].a = acc;
    }
}

void galaxy::setacc1()
{
    int i,j;
    vector r; //vector distance
    double d; //distance
    vector acc;

#pragma omp parallel for private(r,d,acc,j)
    for (i=0;i<n;i++) {
        acc.clear(); 
        for (j=0;j<n;j++) { // cela[j]'s gravity on cela[i]
            if (j != i) { //Not myself
                r = celas[j].p1 - celas[i].p1;
                d = max(r.mag(), celas[j].r + celas[i].r);
                acc += G * celas[j].m * r / (r.mag() * d * d);
            }
        }
        celas[i].a *= (1 - omega);
        celas[i].a += omega * acc;
    }
}


void galaxy::setcollision()
{
    int i,j;
    vector r; //vector distance
    double d; //distance
    vector epi; // unit vector in direction of p[j]-p[i]
    vector dvi,dvj;

    for (i=0;i<n;i++) {
        if (celas[i].c) {
            continue;
        }
        for (j=0;j<i;j++) {
            r = celas[j].p - celas[i].p;
            d = r.mag();
            epi = r / d;
            if ((d < (celas[i].r + celas[j].r)) && !celas[j].c) { //Collision with uncollided one
                celas[i].c = true;
                celas[j].c = true;
                if (r * (celas[j].v - celas[i].v) > 0) {
                    dvj = 2 * celas[i].m / (celas[j].m + celas[i].m) * (celas[i].v - celas[j].v) * epi * epi;
                    dvi = 2 * celas[j].m / (celas[j].m + celas[i].m) * (celas[j].v - celas[i].v) * epi * epi;
                    celas[i].v += dvi;
                    celas[j].v += dvj;
                }
                break;
            }
        }
    }
}

void galaxy::calculateEnergy() 
{
    int i,j;
    ep = 0;
    double eki = 0;
    double epi = 0;
#pragma omp parallel for private(j) reduction(+:eki,epi)
    for (i=0;i<n;i++) {
        eki += celas[i].m * (celas[i].v * celas[i].v) / 2;
        for (j=0;j<i;j++) {
            epi += -G * celas[i].m * celas[j].m / max((celas[j].p - celas[i].p).mag(), celas[j].r + celas[i].r);
        }
    }
    ek = eki;
    ep = epi;
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

#pragma omp parallel for
    for (i=0;i<n;i++) {
        celas[i].c = false;
    }
    
    setacc();
    setcollision();

    for (rec=0;rec<recurdepth;rec++) { //Recursive calculation
#pragma omp parallel for
        for (i=0;i<n;i++) {
            celas[i].newp1(dt);
        }
        setacc1();
    }

#pragma omp parallel for
    for (i=0;i<n;i++) { //Flush back
        celas[i].newp1(dt);
        celas[i].flush(dt);
    }

    if (applyenergyfix) {  // Fix system energy
        this->calculateEnergy();
        co = sqrt((e0 - ep) / ek);
#pragma omp parallel for
        for (i=0;i<n;i++) {
            celas[i].v *= co;
        }
    }

    t += dt;
}
