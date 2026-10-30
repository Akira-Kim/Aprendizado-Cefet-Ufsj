#include <stdio.h>

int potencia(int x, int y) {
    if (y == 0) return 1;
    return x * potencia(x, y - 1);
}

int main() {
    int x, y;
    printf("Digite a base (x): ");
    scanf("%d", &x);
    printf("Digite o expoente (y): ");
    scanf("%d", &y);
    printf("%d^%d = %d\n", x, y, potencia(x, y));
    return 0;
}