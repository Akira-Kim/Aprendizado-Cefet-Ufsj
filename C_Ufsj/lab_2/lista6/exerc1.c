#include <stdio.h>
#include <stdlib.h>

int main()
{
    int N;

    printf("Digite um numero inteiro positivo N: ");
    scanf("%d", &N);

    for (int i = 1; i <= N; i++)
    {

        for (int j = 1; j <= i; j++)
        {

            if (j > 1)
            {
                printf(", ");
            }

            printf("%d", i);
        }

        printf("\n");
    }

    return 0;
}