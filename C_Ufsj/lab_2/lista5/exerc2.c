#include <stdio.h>
#include <stdlib.h>

int main()
{

    int nfinal, cont;

    printf("Escreva um numero para contar ate ele:\n");

    scanf("%d", &nfinal);

    for (cont = nfinal;cont >= 0;cont--){
        printf("\n%d ",cont);
    }

    return 0;
}