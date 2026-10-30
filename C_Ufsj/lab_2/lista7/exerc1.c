#include <stdio.h>
#include <stdlib.h>

float celcios(float f)
{

    float c;
    c = (f - 32.0) * (5.0 / 9.9);

    return c;
}

int main()
{

    float f, c;

    printf("Escreva uma temperatura em Fahrenheit: ");
    scanf("%f", &f);
    c = celcios(f);
    printf("\n\n______________________________________");
    printf("\nCelcios: %2.f\n\n", c);

    return 0;
}