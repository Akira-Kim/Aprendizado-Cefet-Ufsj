#include <stdio.h>
#include <stdlib.h>

int main()
{

    int n = 0, acumulador, cont = 0;

    printf("Escreva numeros possitivos para saber sua media. Para encerrar escreva um numero qualquer negativo.");

    do
    {

        printf("\n********************************************");
        printf("\n*                                          *");
        printf("\n                PROXIMO NUMERO:             \n");
        printf("                    ");
        scanf("%d", &n);

        if (n >= 0)
        {
            acumulador = acumulador + n;
            cont++;
        }

    } while (n >= 0);

    n = acumulador / cont;

    printf("\n\n                            A media é:\n\n                                    %d\n\n\n\n", n);

    return 0;
}