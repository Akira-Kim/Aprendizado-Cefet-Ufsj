#include <stdio.h>
#include <stdlib.h>

int main()
{

    int cont, valor = 0;

    for (cont = 0; cont <= 1000; cont++)
    {

        if (cont % 7 == 0)
        {

            valor = valor + 1;
        }
    }

    printf("********************************************");
    printf("\n*                                          *");
    printf("\n*                  %d                     *", valor);
    printf("\n*                                          *");
    printf("\n********************************************\n\n");

    return 0;
}