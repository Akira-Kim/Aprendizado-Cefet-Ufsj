#include <stdlib.h>
#include <stdio.h>

void zeraNegativos(int v[], int n)
{

    for (int i = 0; i < n; i++)
    {
        if (v[i] < 0)
        {

            v[i] = 0;
        }
    }
}

void mostra_matriz(int v[], int n)
{

    for (int i = 0; i < n; i++)
    {

        printf("%d\n", v[i]);
    }
}

int main()
{

    int valor = 0;

    scanf("%d", &valor);

    int v[valor];

    for (int i = 0; i < valor; i++)
    {

        scanf("%d", &v[i]);
    }

    zeraNegativos(v, valor);

    mostra_matriz(v, valor);

    return 0;
}