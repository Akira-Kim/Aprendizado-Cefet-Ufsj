#include <stdio.h>

void imprimeExclamacoes(int n) {
    if (n <= 0) return;
    imprimeExclamacoes(n - 1);
    for (int i = 0; i < n; i++) {
        printf("!");
    }
    printf("\n");
}

int main() {
    int n;
    printf("Digite um número: ");
    scanf("%d", &n);
    imprimeExclamacoes(n);
    return 0;
}