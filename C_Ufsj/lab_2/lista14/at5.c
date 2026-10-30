#include <stdio.h>

void decToBin(int n) {
    if (n == 0) return;
    decToBin(n / 2);
    printf("%d", n % 2);
}

int main() {
    int n;
    printf("Digite um número decimal: ");
    scanf("%d", &n);
    if (n == 0) printf("0");
    else decToBin(n);
    printf("\n");
    return 0;
}