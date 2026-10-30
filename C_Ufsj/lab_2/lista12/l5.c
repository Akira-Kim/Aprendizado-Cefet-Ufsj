#include <stdio.h>

void multiplicar_matrizes(int a[10][10], int b[10][10], int resultado[10][10]) {
    for (int i = 0; i < 10; i++) {
        for (int j = 0; j < 10; j++) {
            resultado[i][j] = 0;
            for (int k = 0; k < 10; k++) {
                resultado[i][j] += a[i][k] * b[k][j];
            }
        }
    }
}

int main() {
    int a[10][10], b[10][10], resultado[10][10];
    
    printf("Entre com os elementos da matriz A 10x10:\n");
    for (int i = 0; i < 10; i++) {
        for (int j = 0; j < 10; j++) {
            scanf("%d", &a[i][j]);
        }
    }
    
    printf("Entre com os elementos da matriz B 10x10:\n");
    for (int i = 0; i < 10; i++) {
        for (int j = 0; j < 10; j++) {
            scanf("%d", &b[i][j]);
        }
    }
    
    multiplicar_matrizes(a, b, resultado);
    
    printf("Matriz resultado da multiplicação:\n");
    for (int i = 0; i < 10; i++) {
        for (int j = 0; j < 10; j++) {
            printf("%d ", resultado[i][j]);
        }
        printf("\n");
    }
    
    return 0;
}