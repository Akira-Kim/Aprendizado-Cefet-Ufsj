#include <stdio.h>

void soma_colunas() {
    int matriz[3][3];
    int soma_colunas[3] = {0};
    
   
    printf("Entre com os elementos da matriz 3x3:\n");
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            scanf("%d", &matriz[i][j]);
        }
    }
    

    for (int j = 0; j < 3; j++) {
        for (int i = 0; i < 3; i++) {
            soma_colunas[j] += matriz[i][j];
        }
    }

    printf("Soma das colunas:\n");
    for (int j = 0; j < 3; j++) {
        printf("%d ", soma_colunas[j]);
    }
    printf("\n");
}

int main() {
    soma_colunas();
    return 0;
}