#include <stdio.h>
#include <math.h>


int is_prime(int num) {
    if (num <= 1) {
        return 0; 
    }
    if (num <= 3) {
        return 1;
    }
    if (num % 2 == 0 || num % 3 == 0) {
        return 0; 
    }

    for (int i = 5; i * i <= num; i += 6) {
        if (num % i == 0 || num % (i + 2) == 0) {
            return 0; 
        }
    }
    return 1; 
}

int main() {
    int a, b;
    
    printf("Digite o valor de a: ");
    scanf("%d", &a);
    printf("Digite o valor de b: ");
    scanf("%d", &b);
    
    printf("Números primos no intervalo [%d, %d]: ", a, b);
    
    for (int i = a; i <= b; ++i) {
        if (is_prime(i)) {

            printf("%d, ", i);
        }
    }
    
    printf("\n");

    return 0;
}