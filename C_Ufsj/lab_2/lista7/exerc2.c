#include <stdio.h>
#include <stdlib.h>


float volume(float r)
{

    float v;
    v = ((4/3)*3,14)*(r*r*r);

    return v;
}

int main()
{

    float r, v;

    printf("Escreva uma raio para saber o volume da esfera: ");
    scanf("%f", &r);
    v = volume(r);
    printf("\n\n______________________________________");
    printf("\nVolume: %2.f\n\n", v);

    return 0;
}