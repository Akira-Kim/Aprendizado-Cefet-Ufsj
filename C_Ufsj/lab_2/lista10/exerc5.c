#include <stdlib.h>
#include <stdio.h>

double produto_escalar(double u[], double v[], int n) {
    int i;
    double soma = 0;
    for (i = 0; i < n; i++) {  // Iterate from 0 to n-1
        soma += u[i] * v[i];
    }
    return soma;  // Corrected spelling of return
}

int main() {
    int n, i;
    
    printf("Digite o nuemro de elementos: ");
    scanf("%d", &n);
    
    double vet[n], uet[n], t;
    
    printf("digite os elementos dos dois vetores:\n");
    for (i = 0; i < n; i++) {  
        scanf("%lf %lf", &vet[i], &uet[i]);
    }
    
    t = produto_escalar(uet, vet, n);  
    
    printf("%.2lf\n", t);  
    
    return 0;
}