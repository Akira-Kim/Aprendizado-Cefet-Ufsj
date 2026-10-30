#include <stdio.h>
#include <stdlib.h>

int main()
{

    int a, b = 0, i;

    printf("\n________________________________________\n");
    printf("\nEscreva um numero para saber a soma dos seus divisores:\n");
    printf("________________________________________\n\n");

    scanf("%d", &a);

    for (i = 1; i < a; i++)
    {

        if (a % i == 0)
        {

            b = i + b;
        }
    }
    printf("\n________________________________________\n");
    printf("\n%d\n", b);
    printf("________________________________________\n\n");

    return 0;
}