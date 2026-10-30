#include <stdio.h>
#include <string.h>

#define MAX_TITULO 31
#define MAX_AUTOR 16

typedef struct {
    char titulo[MAX_TITULO];
    char autor[MAX_AUTOR];
    int ano;
} Livro;

void procura_livro(Livro *v, int n, char *autor) {
    int encontrado = 0;
    for (int i = 0; i < n; i++) {
        if (strcmp(v[i].autor, autor) == 0) {
            printf("Título: %s\n", v[i].titulo);
            encontrado = 1;
        }
    }
    if (!encontrado) {
        printf("Nenhum livro encontrado para o autor %s.\n", autor);
    }
}

int main() {
    int n;
    char autor[MAX_AUTOR];

    printf("Digite o número de livros: ");
    scanf("%d", &n);
    getchar();

    Livro livros[n];

    for (int i = 0; i < n; i++) {
        printf("Digite o título do livro %d: ", i + 1);
        fgets(livros[i].titulo, sizeof(livros[i].titulo), stdin);
        livros[i].titulo[strcspn(livros[i].titulo, "\n")] = '\0';

        printf("Digite o autor do livro %d: ", i + 1);
        fgets(livros[i].autor, sizeof(livros[i].autor), stdin);
        livros[i].autor[strcspn(livros[i].autor, "\n")] = '\0';

        printf("Digite o ano do livro %d: ", i + 1);
        scanf("%d", &livros[i].ano);
        getchar();
    }

    printf("Digite o nome do autor para procurar: ");
    fgets(autor, sizeof(autor), stdin);
    autor[strcspn(autor, "\n")] = '\0';

    printf("\nLivros do autor %s:\n", autor);
    procura_livro(livros, n, autor);

    return 0;
}