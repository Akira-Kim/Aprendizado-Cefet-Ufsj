#include <stdio.h>
#include <stdlib.h>
int main()
{

    float n, h, p;

    printf("Digite sua altura:\n");
    scanf("%f", &h);

    printf("Digite seu peso:\n");
    scanf("%f", &p);

    n = p / (h * h);

    printf("%f", n);

    if (n < 18.5)
    {

        printf("\nAbaixo do Peso");
    }
    else if (n > 18.6 && n < 24.9)
    {

        printf("\nSaldavel");
    }
    else if (n > 25 && n < 29.9)
    {

        printf("\nPeso em exesso");
    }
    else if (n > 30 && n < 34.9)
    {

        printf("\nObesidade Grau I");
    }
    else if (n > 35 && n < 39.9)
    {

        printf("\nObesidade Grau II (severa)");
    }
    else if (n >= 40)
    {

        printf("\nObesidade Grau III (mórbida)");
    }
    else
    {

        printf("\nERRO");
    }

    return 0;
}