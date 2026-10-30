#include <stdlib.h>
#include <stdio.h>

int maiorq(int v[], int t)
{

    int m = v[0];

    for (int i = 0; i < t; i++)
    {

        if (m < v[i])
        {

            m = v[i];
        }
    }

    return m;
}

int pq(int v[], int t)
{

    int p, m = v[0];

    for (int i = 0; i < t; i++)
    {

        if (m < v[i])
        {

            m = v[i];

            p = i;
        }
    }

    return p;
}

int main()
{

    int maior, p;

    int valor = 0;

    scanf("%d", &valor);

    int v[valor];

    for (int i = 0; i < valor; i++)
    {

        scanf("%d", &v[i]);
    }

    maior = maiorq(v, valor);

    p = pq(v, valor);

    printf("\n Maior: %d \n Posição: %d\n\n", maior, p + 1);

    return 0;
}