#include <stdio.h>
#include <limits.h>

int main()
{
    int numero;
    int soma = 0;
    int quantidade = 0;
    int maior = INT_MIN, segundo_maior = INT_MIN;
    int menor = INT_MAX, segundo_menor = INT_MAX;

    printf("Digite os números inteiros (digite 0 para encerrar):\n");

    while (1)
    {
        scanf("%d", &numero);

        if (numero == 0)
        {
            break;
        }

        soma += numero;
        quantidade++;

        if (numero > maior)
        {
            segundo_maior = maior;
            maior = numero;
        }
        else if (numero > segundo_maior && numero != maior)
        {
            segundo_maior = numero;
        }

        if (numero < menor)
        {
            segundo_menor = menor;
            menor = numero;
        }
        else if (numero < segundo_menor && numero != menor)
        {
            segundo_menor = numero;
        }
    }

    if (quantidade > 0)
    {

        double media = (double)soma / quantidade;

        printf("\nResultados:\n");
        printf("Soma dos valores: %d\n", soma);
        printf("Média dos valores: %.2f\n", media);
        printf("Maior valor: %d\n", maior);
        printf("Segundo maior valor: %d\n", segundo_maior);
        printf("Menor valor: %d\n", menor);
        printf("Segundo menor valor: %d\n", segundo_menor);
    }
    else
    {
        printf("Nenhum número foi digitado.\n");
    }

    return 0;
}