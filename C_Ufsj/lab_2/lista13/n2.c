#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Uso: %s <arquivo1> <arquivo2>\n", argv[0]);
        return 1;
    }

    FILE *file1 = fopen(argv[1], "r");
    FILE *file2 = fopen(argv[2], "r");
    FILE *file_out = fopen("concatenacao.txt", "w");

    if (file1 == NULL || file2 == NULL || file_out == NULL) {
        printf("Erro ao abrir um dos arquivos.\n");
        return 1;
    }

    char linha[1024];

    
    while (fgets(linha, sizeof(linha), file1) != NULL) {  
        fprintf(file_out, "%s", linha);  
    }
    fclose(file1);

    while (fgets(linha, sizeof(linha), file2) != NULL) {
        fprintf(file_out, "%s", linha);
    }
    fclose(file2);

    fclose(file_out);
    printf("Arquivos concatenados com sucesso em concatenacao.txt.\n");
    return 0;
}