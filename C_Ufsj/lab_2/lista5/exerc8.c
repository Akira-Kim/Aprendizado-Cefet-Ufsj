#include <stdio.h>
#include <stdlib.h>

int main()
{

    int s, s1, resto = 0;

    printf("\n________________________________________\n");
    printf("\nDigite dois numeros para descobrir se são primos entre si:\n");
    printf("________________________________________\n\n");

    scanf("%d", &s);
    scanf("%d", &s1);

    while (s1 != 0)
    {

        resto = s % s1;
        s = s1;
        s1 = resto;

        
    }

    if (s == 1)
    {
        printf("\n________________________________________\n");
        printf("\n Eles são primos entre si");
        printf("\n________________________________________");
    }
    else
    {
        printf("\n________________________________________\n");
        printf("\n Eles não são primos entre si");
        printf("\n________________________________________");
    }
    

    return 0;
}