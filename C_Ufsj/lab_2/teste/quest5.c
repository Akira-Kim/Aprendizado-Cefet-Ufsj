#include <stdio.h>

int main()
{
    int a, b;
    int resultado;

    printf("Digite o valor de a: ");
    scanf("%d", &a);
    printf("Digite o valor de b: ");
    scanf("%d", &b);

    resultado = (b * b * b + a * b) - 2 * b + a % b;

    printf("O resultado da expressão é: %d\n", resultado);

    return 0;
}