#include <stdio.h>
#include <string.h>

void imprimeSegmento(const char *S, int i, int j) {
    int len = strlen(S);

    if (i < 0 || j < 0 || i >= len || j >= len || i > j) {
        printf("Índices fora dos limites ou inválidos.\n");
        return;
    }

    for (int k = i; k <= j; k++) {
        putchar(S[k]);
    }
    printf("\n");
}

int main() {
    char S[100];
    int i, j;

    printf("Digite uma string: ");
    fgets(S, sizeof(S), stdin);

  
    S[strcspn(S, "\n")] = '\0';

    printf("Digite o índice inicial (i): ");
    scanf("%d", &i);
    printf("Digite o índice final (j): ");
    scanf("%d", &j);

    imprimeSegmento(S, i, j);

    return 0;
}