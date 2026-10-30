#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Uso: %s <nome_do_arquivo>\n", argv[0]);
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if (file == NULL) {
        printf("Erro ao abrir o arquivo %s.\n", argv[1]);
        return 1;
    }

    char nome[100];
    int quantidade;
    float preco, total = 0.0;

    while (fscanf(file, "%[^,],%d,%f\n", nome, &quantidade, &preco) == 3) {
        total += quantidade * preco;
    }

    fclose(file);
    printf("Total da compra: R$%.2f\n", total);
    return 0;
}