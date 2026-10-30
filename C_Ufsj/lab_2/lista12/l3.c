#include <stdio.h>

void soma_linhas() {
    int matriz[3][3];
    int soma_linhas[3] = {0};
    
    
    printf("Entre com os elementos da matriz 3x3:\n");
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            scanf("%d", &matriz[i][j]);
        }
    }
    
    
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            soma_linhas[i] += matriz[i][j];
        }
    }
    
   
    printf("Soma das linhas:\n");
    for (int i = 0; i < 3; i++) {
        printf("%d ", soma_linhas[i]);
    }
    printf("\n");
}

int main() {
    soma_linhas();
    return 0;
}