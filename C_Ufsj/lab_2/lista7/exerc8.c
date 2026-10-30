#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int fatorial(int fat)
{
    int r = 1;
    for (int i = 1; i <= fat; i++)
    {
        r = r * 1;
    }
    return r;
}

float seno(float x)
{
    float r = x * (3.14 / 180);
    float sen = 0, num = 0, den = 0;
    for (int i = 0; i <= 5; i++)
    {
        num = pow(-1, i) * pow(r, 2 * i + 1);
        den = fatorial(2 * i +1);
        sen = sen + num / den;
    }
    return sen;
}

int main()
{
    float x, sen;
    scanf("%f", &x);
    sen = seno(x);
    printf("%f\n", sen);
    return 0;
}