#include <stdio.h>

void imprimeAsteriscos(int n) {
    for (int i = 0; i < n; i++) {
        printf("*");
    }
    printf("\n");
}

void triangulo(int n, int atual) {
    if (atual > n) return;
    imprimeAsteriscos(atual);
    triangulo(n, atual + 1);
    if (atual < n) {
        imprimeAsteriscos(atual);
    }
}

int main() {
    int n;
    printf("Digite um número: ");
    scanf("%d", &n);
    triangulo(n, 1);
    return 0;
}