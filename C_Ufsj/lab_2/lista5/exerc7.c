#include <stdio.h>
#include <stdlib.h>


int fibonacci(int n) {
    if (n <= 1){
        return n; 
    }

    int s = 0, s1 = 1, nfibon = 0;

    
    for (int i = 2; i <= n; ++i) {
        nfibon = s + s1;
        s = s1;
        s1 = nfibon;
    }

    return nfibon;
}

int main() {

    int p, r;

    printf("************************************************\n\n");
    printf("Digite a posição na sequência de Fibonacci: ");
    scanf("%d", &p);
    printf("\n************************************************\n");

    if (p < 0) {
        printf("ERRO\n");
        return 1; 
    }

    r = fibonacci(p);


    printf("\n-----------------------------------------------------");
    printf("\n               Na posição %d é: %d", p, r);
    printf("\n-----------------------------------------------------\n\n\n\n");

    return 0;
}