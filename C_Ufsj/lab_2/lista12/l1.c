#include <stdio.h>

void matriz_diagonal_principal() {
    int matriz[5][5];
    
    
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            matriz[i][j] = 0;
        }
    }
    
   
    for (int i = 0; i < 5; i++) {
        matriz[i][i] = 1;
    }

    printf("Matriz 5x5 com diagonal principal 1:\n");
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            printf("%d ", matriz[i][j]);
        }
        printf("\n");
    }
}

int main() {
    matriz_diagonal_principal();
    return 0;
}