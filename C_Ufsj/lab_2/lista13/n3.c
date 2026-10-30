#include <stdio.h>
#include <ctype.h>

int num_vogais_arquivo(char *nome_arq) {
    FILE *file = fopen(nome_arq, "r");
    if (file == NULL) {
        printf("Erro ao abrir o arquivo %s.\n", nome_arq);
        return -1;
    }

    int vogais = 0;
    char ch;
    while ((ch = fgetc(file)) != EOF) {
        ch = tolower(ch);
        if (ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u') {
            vogais++;
        }
    }

    fclose(file);
    return vogais;
}

int main() {
    char nome_arquivo[100];
    printf("Digite o nome do arquivo: ");
    scanf("%s", nome_arquivo);
    int resultado = num_vogais_arquivo(nome_arquivo);
    if (resultado != -1) {
        printf("O arquivo %s tem %d vogais.\n", nome_arquivo, resultado);
    }
    return 0;
}