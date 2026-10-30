#include <stdio.h>

#define MAX_TITULO 100

typedef struct Filme {
    char titulo[MAX_TITULO];
    int duracao;
    int ano;
} Filme;

void lista_filmes(Filme filmes[], int n) {
    for (int i = 0; i < n; i++) {
        printf("Título: %s\n", filmes[i].titulo);
        printf("Duração: %d minutos\n", filmes[i].duracao);
        printf("Ano: %d\n", filmes[i].ano);
        printf("-------------------------\n");
    }
}

void lista_filmes_ano(Filme filmes[], int n, int ano) {
    int encontrou = 0;
    for (int i = 0; i < n; i++) {
        if (filmes[i].ano == ano) {
            printf("Título: %s\n", filmes[i].titulo);
            printf("Duração: %d minutos\n", filmes[i].duracao);
            printf("Ano: %d\n", filmes[i].ano);
            printf("-------------------------\n");
            encontrou = 1;
        }
    }
    if (!encontrou) {
        printf("Nenhum filme encontrado para o ano %d.\n", ano);
    }
}

void lista_filmes_duracao(Filme filmes[], int n, int duracao) {
    int encontrou = 0;
    for (int i = 0; i < n; i++) {
        if (filmes[i].duracao < duracao) {
            printf("Título: %s\n", filmes[i].titulo);
            printf("Duração: %d minutos\n", filmes[i].duracao);
            printf("Ano: %d\n", filmes[i].ano);
            printf("-------------------------\n");
            encontrou = 1;
        }
    }
    if (!encontrou) {
        printf("Nenhum filme encontrado com duração menor que %d minutos.\n", duracao);
    }
}

int main() {
    int n;

    printf("Digite o número de filmes: ");
    scanf("%d", &n);
    getchar();

    Filme filmes[n];

    for (int i = 0; i < n; i++) {
        printf("Digite o título do filme %d: ", i + 1);
        fgets(filmes[i].titulo, sizeof(filmes[i].titulo), stdin);
        filmes[i].titulo[strcspn(filmes[i].titulo, "\n")] = '\0';

        printf("Digite a duração (em minutos) do filme %d: ", i + 1);
        scanf("%d", &filmes[i].duracao);
        getchar();

        printf("Digite o ano do filme %d: ", i + 1);
        scanf("%d", &filmes[i].ano);
        getchar();
    }

    int ano;
    printf("\nDigite o ano para procurar filmes: ");
    scanf("%d", &ano);
    getchar();
    printf("\nFilmes do ano %d:\n", ano);
    lista_filmes_ano(filmes, n, ano);

    int duracao;
    printf("\nDigite a duração máxima para procurar filmes: ");
    scanf("%d", &duracao);
    getchar();
    printf("\nFilmes com duração menor que %d minutos:\n", duracao);
    lista_filmes_duracao(filmes, n, duracao);

    return 0;
}