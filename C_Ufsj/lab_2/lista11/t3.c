#include <stdio.h>

int contaVogais(char *texto)
{
    int contador = 0;
    char c;

    while ((c = *texto++) != '\0')
    {
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' ||
            c == 'A' || c == 'E' || c == 'I' || c == 'O' || c == 'U')
        {
            contador++;
        }
    }

    return contador;
}

int main()
{
    char texto[100];

    printf("Digite uma string: ");
    fgets(texto, sizeof(texto), stdin);

    int numero_vogais = contaVogais(texto);
    printf("Número de vogais: %d\n", numero_vogais);

    return 0;
}