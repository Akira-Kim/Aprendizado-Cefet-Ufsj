#include <stdio.h>

int main() {
    char str[100];

    printf("Digite uma string: ");
    fgets(str, sizeof(str), stdin);

    printf("As quatro primeiras letras são: ");
    for (int i = 0; i < 4 && str[i] != '\0' && str[i] != '\n'; i++) {
        putchar(str[i]);
    }
    printf("\n");

    return 0;
}