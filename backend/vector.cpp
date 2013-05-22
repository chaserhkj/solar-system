#include "vector.h"
#include <cmath>

vector vector::operator+ (const vector &v) const
{
    return vector(x+v.x, y+v.y, z+v.z);
}

void vector::operator+= (const vector &v)
{
    x += v.x;
    y += v.y;
    z += v.z;
}

vector vector::operator- (const vector &v) const
{
    return vector(x-v.x,y-v.y,z-v.z);
}

void vector::operator-= (const vector &v)
{
    x -= v.x;
    y -= v.y;
    z -= v.z;
}

vector vector::operator* (double s) const
{
    return vector(x*s, y*s, z*s);
}

void vector::operator*= (double s)
{
    x *= s;
    y *= s;
    z *= s;
}

vector vector::operator/ (double s) const
{
    return vector(x/s, y/s, z/s);
}

void vector::operator/= (double s)
{
    x /= s;
    y /= s;
    z /= s;
}

double vector::operator* (const vector &v) const
{
    return x*v.x+y*v.y+z*v.z;
}

bool vector::operator== (const vector &v) const
{
    return ((x==v.x) && (y==v.y) && (z==v.z));
}
double vector::mag() const
{
    return sqrt(x*x+y*y+z*z);
}

vector operator* (double s, const vector &v)
{
    return vector(v.x*s, v.y*s, v.z*s);
}

