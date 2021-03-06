//Copyright (C) 2013 Kangjing Huang & Zhiyi Xu
//For further infomation, see LICENSE.txt

#ifndef VECTOR_H
#define VECTOR_H

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
    void clear(); // =(0,0,0)
    
};

vector operator* (double s, const vector &v);

#endif //VECTOR_H
