#include <stdio.h>

typedef struct {
    int id;
    int duracao;
    int ano;
} Filme;

void imprime_filme(Filme filmes[], int n, int id) {
    for (int i = 0; i < n; i++) {
        if (filmes[i].id == id) {
            printf("Ano: %d\n", filmes[i].ano);
            printf("Duração: %d\n", filmes[i].duracao);
            return;
        }
    }
    printf("Filme com id %d não existe\n", id);
}

int main() {
    int n;
    printf("Digite o número de filmes: ");
    scanf("%d", &n);

    Filme filmes[n];

    printf("Digite as informações dos filmes (id duracao ano):\n");
    for (int i = 0; i < n; i++) {
        scanf("%d %d %d", &filmes[i].id, &filmes[i].duracao, &filmes[i].ano);
    }

    int id;
    printf("Digite o id do filme a ser pesquisado: ");
    scanf("%d", &id);

    imprime_filme(filmes, n, id);

    return 0;
}