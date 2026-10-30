#include <stdio.h>

void separaParesImpares(unsigned int v[], int tam) {
    int i = 0;
    int j = tam - 1;

    while (i < j) {
        while (i < tam && v[i] % 2 == 0) {
            i++;
        }
        while (j >= 0 && v[j] % 2 != 0) {
            j--;
        }
        if (i < j) {
            unsigned int temp = v[i];
            v[i] = v[j];
            v[j] = temp;
        }
    }
}

int main() {
    int tam;
    printf("Digite o tamanho do vetor: ");
    scanf("%d", &tam);

    unsigned int v[tam];

    printf("Digite os elementos do vetor:\n");
    for (int i = 0; i < tam; i++) {
        scanf("%u", &v[i]);
    }

    separaParesImpares(v, tam);

    printf("Vetor após separação de pares e ímpares:\n");
    for (int i = 0; i < tam; i++) {
        printf("%u ", v[i]);
    }
    printf("\n");

    return 0;
}