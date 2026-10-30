#include <stdlib.h>
#include <stdio.h>
#include <time.h>

int preencheVet(int v[], int t)
{

    srand(time(NULL));

    for (int i = 0; i < t; i++)
    {

        v[i] = rand();
    }

    return v[t];
}

float media(int v[], int t)
{

    int soma = 0;
    float media = 0;

    for (int i = 0; i < t; i++)
    {

        soma += v[i];
    }

    media = soma / t;

    return media;
}

int main()
{

    int tam;
    float med = 0;

    scanf("%d", &tam);

    int vet[tam];

    vet[tam] = preencheVet(vet, tam);

    med = media(vet, tam);

    printf("\n%2.f\n\n", med);

    return 0;
}
