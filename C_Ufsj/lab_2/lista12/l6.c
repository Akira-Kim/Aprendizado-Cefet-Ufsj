#include <stdio.h>

double soma_diagonal_principal(double m[100][100], int tamanho) {
    double soma = 0;
    for (int i = 0; i < tamanho; i++) {
        soma += m[i][i];
    }
    return soma;
}

int main() {
    double matriz[100][100];
    int tamanho;
    
    printf("Entre com o tamanho da matriz (máximo 100): ");
    scanf("%d", &tamanho);
    
    if (tamanho > 100) {
        printf("Tamanho da matriz deve ser no máximo 100.\n");
        return 1;
    }
    
    printf("Entre com os elementos da matriz %d x %d:\n", tamanho, tamanho);
    for (int i = 0; i < tamanho; i++) {
        for (int j = 0; j < tamanho; j++) {
            scanf("%lf", &matriz[i][j]);
        }
    }
    
    double resultado = soma_diagonal_principal(matriz, tamanho);
    printf("Soma dos elementos da diagonal principal: %.2f\n", resultado);
    
    return 0;
}