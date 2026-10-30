#include <stdio.h>

void substituir(char *texto, char letra)
{
    while (*texto != '\0')
    {
        if (*texto == 'a' || *texto == 'e' || *texto == 'i' || *texto == 'o' || *texto == 'u' ||
            *texto == 'A' || *texto == 'E' || *texto == 'I' || *texto == 'O' || *texto == 'U')
        {
            *texto = letra;
        }
        texto++;
    }
}

int main()
{
    char texto[100];
    char letra;

    printf("Digite uma string: ");
    fgets(texto, sizeof(texto), stdin);

    printf("Digite a letra para substituir as vogais: ");
    scanf("%c", &letra);

    substituir(texto, letra);

    printf("Texto após substituição: %s\n", texto);

    return 0;
}