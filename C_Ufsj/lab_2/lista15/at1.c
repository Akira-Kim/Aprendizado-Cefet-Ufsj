#include <stdio.h>
#include <stdlib.h>

int *cria_inteiro(int n) {
    int *p = (int *)malloc(sizeof(int));
    *p = n;
    return p;
}

int main() {
    int *p = cria_inteiro(5);
    printf("%d\n", *p);
    free(p);
    return 0;
}