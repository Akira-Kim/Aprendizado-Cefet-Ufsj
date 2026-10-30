#include <stdio.h>

#define MAX_LEN 16  // +1 para o caractere nulo

typedef struct {
    char modelo[MAX_LEN];
    char marca[MAX_LEN];
    int ano;
    double preco;
} Carro;

void listaCarros(Carro *carros, int n, double x) {
    for (int i = 0; i < n; i++) {
        if (carros[i].preco <= x) {
            printf("Modelo: %s\n", carros[i].modelo);
        }
    }
}

int main() {
    int n;
    double preco_max;

    printf("Digite o número de carros: ");
    scanf("%d", &n);

    Carro carros[n];

    for (int i = 0; i < n; i++) {
        printf("Digite o modelo do carro %d: ", i + 1);
        scanf("%s", carros[i].modelo);
        
        printf("Digite a marca do carro %d: ", i + 1);
        scanf("%s", carros[i].marca);

        printf("Digite o ano do carro %d: ", i + 1);
        scanf("%d", &carros[i].ano);

        printf("Digite o preço do carro %d: ", i + 1);
        scanf("%lf", &carros[i].preco);
    }

    printf("Digite o valor máximo para o preço dos carros: ");
    scanf("%lf", &preco_max);

    printf("\nCarros com preço menor ou igual a %.2f:\n", preco_max);
    listaCarros(carros, n, preco_max);

    return 0;
}