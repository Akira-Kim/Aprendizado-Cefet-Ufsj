#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <locale.h>
#include <string.h>

#define SIZE 9
#define SUBGRIDSIZE 3
#define EMPTY 0
#define NICK_SIZE 25
int dicas[SIZE][SIZE];

void salvaDicas(int grid[SIZE][SIZE]){
    for (int i = 0; i < SIZE; i++)
    {
        for (int j = 0; j < SIZE; j++)
        {
            dicas[i][j] = grid[i][j];
        }
        
    }
    
}

// Função para exibir o grid
void exibirGrid(int grid[SIZE][SIZE])
{
    printf("\n");
    printf("    ---------------------------------\n");
    printf("    *            SUDOKU             *\n");
    printf("    ---------------------------------\n");
    printf("     ");
    for (int j = 1; j <= SIZE; j++)
    {
        if (j==3||j==6||j==9)
        {
            printf(" %i    ", j);
        }else printf(" %i ", j);
    }
    printf("\n");
    printf("    ---------------------------------\n");
    for (int i = 0; i < SIZE; i++)
    {
        if (i % SUBGRIDSIZE == 0 && i != 0)
        {
            printf("    ---------------------------------\n");
        }

        printf(" %d  |", i+1); // Exibir número da linha

        for (int j = 0; j < SIZE; j++)
        {
            if (j % SUBGRIDSIZE == 0 && j != 0)
            {
                printf(" | ");
            }
            if (grid[i][j] == EMPTY)
            {
                printf(" . ");
            }
            else
            {
                printf(" %d ", grid[i][j]);
            }
        }
        printf("\n");
    }
    printf("\n");
}

// Função para verificar se um número pode ser colocado na posição (linha, coluna)
int podeColocar(int grid[SIZE][SIZE], int linha, int coluna, int num)
{
    // Verificar a linha
    for (int i = 0; i < SIZE; i++)
    {
        if (grid[linha][i] == num)
        {
            return 0;
        }
    }
    // Verificar a coluna
    for (int i = 0; i < SIZE; i++)
    {
        if (grid[i][coluna] == num)
        {
            return 0;
        }
    }
    // Verificar o quadrante 3x3
    int startRow = linha - linha % SUBGRIDSIZE;
    int startCol = coluna - coluna % SUBGRIDSIZE;
    for (int i = startRow; i < startRow + SUBGRIDSIZE; i++)
    {
        for (int j = startCol; j < startCol + SUBGRIDSIZE; j++)
        {
            if (grid[i][j] == num)
            {
                return 0;
            }
        }
    }
    return 1;
}

void embaralharVetor(int arr[], int tamanho)
{
    for (int i = tamanho - 1; i > 0; i--)
    {
        int j = rand() % (i + 1);
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}

// Função para verificar o número usando backtracking
int resolverSudoku(int grid[SIZE][SIZE])
{
    int linha, coluna;

    // Encontrar a primeira célula vazia
    for (linha = 0; linha < SIZE; linha++)
    {
        for (coluna = 0; coluna < SIZE; coluna++)
        {
            if (grid[linha][coluna] == EMPTY)
            {
                // Criar um vetor de números de 1 a 9
                int numeros[SIZE];
                for (int i = 0; i < SIZE; i++)
                {
                    numeros[i] = i + 1;
                }

                // Embaralhar o vetor de números
                embaralharVetor(numeros, SIZE);

                // Tentar números aleatórios
                for (int i = 0; i < SIZE; i++)
                {
                    int num = numeros[i];
                    if (podeColocar(grid, linha, coluna, num))
                    {
                        grid[linha][coluna] = num;
                        if (resolverSudoku(grid))
                        {
                            return 1;
                        }
                        grid[linha][coluna] = EMPTY;
                    }
                }
                return 0; // Se nenhum número é válido, retorna 0
            }
        }
    }

    return 1; // Sudoku resolvido
}

// Função para gerar um Sudoku válido com uma solução única
void gerarSudoku(int grid[SIZE][SIZE])
{
    // Inicializar o grid com zeros
    for (int i = 0; i < SIZE; i++)
    {
        for (int j = 0; j < SIZE; j++)
        {
            grid[i][j] = EMPTY;
            dicas[i][j] = EMPTY;
        }
    }

    // Preencher o grid usando backtracking
    resolverSudoku(grid);
}

int verificarSudoku(int grid[SIZE][SIZE])
{
    int numeros[SIZE];

    // Verificar linhas e colunas
    for (int i = 0; i < SIZE; i++)
    {
        // Reinicializar o array de verificação
        for (int j = 0; j < SIZE; j++)
            numeros[j] = 0;

        // Verificação da linha
        for (int j = 0; j < SIZE; j++)
        {
            int num = grid[i][j];
            if (num < 1 || num > SIZE || numeros[num - 1] != 0)
            {
                return 0; // Número inválido ou repetido na linha
            }
            numeros[num - 1] = 1;
        }

        // Reinicializar o array de verificação para a coluna
        for (int j = 0; j < SIZE; j++)
            numeros[j] = 0;

        // Verificação da coluna
        for (int j = 0; j < SIZE; j++)
        {
            int num = grid[j][i];
            if (num < 1 || num > SIZE || numeros[num - 1] != 0)
            {
                return 0; // Número inválido ou repetido na coluna
            }
            numeros[num - 1] = 1;
        }
    }

    // Verificar subgrades 3x3
    for (int linha = 0; linha < SIZE; linha += 3)
    {
        for (int coluna = 0; coluna < SIZE; coluna += 3)
        {
            // Reinicializar o array de verificação para a subgrade
            for (int j = 0; j < SIZE; j++)
                numeros[j] = 0;

            // Verificação da subgrade
            for (int i = 0; i < 3; i++)
            {
                for (int j = 0; j < 3; j++)
                {
                    int num = grid[linha + i][coluna + j];
                    if (num < 1 || num > SIZE || numeros[num - 1] != 0)
                    {
                        return 0; // Número inválido ou repetido na subgrade
                    }
                    numeros[num - 1] = 1;
                }
            }
        }
    }

    return 1; // Sudoku válido
}

// Função para escolher a dificuldade
int dificuldade()
{
    int dif;
    printf(" ----------------------------\n");
    printf(" *  Escolha a dificuldade:  *\n");
    printf(" ----------------------------\n");
    printf(" *                          *\n");
    printf(" *        1. Facil          *\n");
    printf(" *        2. Medio          *\n");
    printf(" *        3. Dificil        *\n");
    printf(" *                          *\n");
    printf(" ----------------------------\n\n");
    printf(" -> ");
    scanf("%d", &dif);
    return dif;
}

void level(int dif, int grid[SIZE][SIZE])
{
    int numPistas;
    switch (dif)
    {
    case 1:                                    // Fácil
        numPistas = (int)(SIZE * SIZE) * 0.60; // ~60% preenchido
        break;
    case 2:                                    // Médio
        numPistas = (int)(SIZE * SIZE) * 0.50; // 50% preenchido
        break;
    case 3:                                    // Difícil
        numPistas = (int)(SIZE * SIZE) * 0.40; // ~40% preenchido
        break;
    default:
        numPistas = (int)(SIZE * SIZE) * 0.60; // Padrão fácil
        break;
    }

    // Remover algumas pistas para ajustar a dificuldade
    int numRemovidos = SIZE * SIZE - numPistas;
    while (numRemovidos > 0)
    {
        int linha = rand() % SIZE;
        int coluna = rand() % SIZE;
        if (grid[linha][coluna] != EMPTY)
        {
            grid[linha][coluna] = EMPTY;
            numRemovidos--;
        }
    }

    salvaDicas(grid);
}
// Função pra remover nmrs

int removerNumeros(int grid[SIZE][SIZE])
{
    int linha, coluna;
    char continuarRemovendo;
    do
    {
        printf(" Digite a linha a ser alterada (1-9): ");
        printf("\n\n -> ");
        scanf("%d", &linha);
        linha--;
        printf(" Digite a coluna a ser alterada(1-9): ");
        printf("\n\n -> ");
        scanf("%d", &coluna);
        coluna--;

        if (grid[linha][coluna] != EMPTY && dicas[linha][coluna]==EMPTY)
        {
            grid[linha][coluna] = EMPTY;
            exibirGrid(grid);
            printf("\n\n Numero removido.");
        }
        else
        {
            printf("\n\n A celula ja está vazia ou é uma dica. Tente novamente.");
            continue;
        }

        printf("\n\n Deseja continuar removendo? (s/n)");
        printf("\n\n -> ");
        scanf(" %c", &continuarRemovendo);
        if (continuarRemovendo == 'n' || continuarRemovendo == 'N')
        {
            return 0;
        }

    } while (continuarRemovendo == 'S' || continuarRemovendo == 's');
}

// Função para permitir que o usuário jogue
int jogar(int grid[SIZE][SIZE])
{
    int linha, coluna, num;
    char continuarJogando, removerNum;

    exibirGrid(grid);

    do
    {
        printf("\n Digite a linha (1-9): ");
        printf("\n\n -> ");
        scanf("%d", &linha);
        linha--;
        printf("\n Digite a coluna (1-9): ");
        printf("\n\n -> ");
        scanf("%d", &coluna);
        coluna--;
        printf("\n Digite o numero (1-9): ");
        printf("\n\n -> ");
        scanf("%d", &num);

        if (linha < 0 || linha >= SIZE || coluna < 0 || coluna >= SIZE || num < 1 || num > SIZE)
        {
            printf("\n > Entrada invalida. Tente novamente.\n");
            continue;
        }

        if (grid[linha][coluna] == EMPTY)
        {
            grid[linha][coluna] = num;
            exibirGrid(grid);
        }
        else
        {
            printf("\n > A celula ja esta preenchida. Tente novamente.\n");
            
        }

        do
        {
            printf("\n  Deseja remover algum numero? (s/n): ");
            printf("\n\n -> ");
            scanf(" %c", &removerNum);

            if (removerNum == 's' || removerNum == 'S')
            {
                removerNumeros(grid);
                break;
            }
            if (removerNum == 'n' || removerNum == 'N')
            {
                break;
            }
            else
            {
                printf("\n Caracter invalido. Tente Novamente.");
                continue;
            }

        } while (removerNum == 's' || removerNum == 'S');

        do
        {
            printf("\n Deseja continuar jogando? (s/n): \n");
            printf("\n -> ");
            scanf(" %c", &continuarJogando);

            if (continuarJogando == 'n' || continuarJogando == 'N')
            {
                char verificar;

                printf("\n Deseja verificar o sudoku? (s/n)");
                printf("\n\n -> ");
                scanf(" %c", &verificar);
                if (verificar == 's' || verificar == 'S')
                {
                    for (int i = 0; i < SIZE; i++)
                    {
                        for (int j = 0; j < SIZE; j++)
                        {
                            if (grid[i][coluna] != EMPTY && grid[linha][j] != EMPTY)
                            {
                                int verificar = verificarSudoku(grid);
                                if (verificar == 1)
                                {

                                    printf("\n > Sudoku preenchido com sucesso!");
                                    return 1;
                                }
                                else if (grid[i][coluna] == EMPTY || grid[linha][j] == EMPTY)
                                {

                                    printf("\n > Jogo incompleto. Tente Novamente.\n");
                                    break;
                                }
                                else
                                {
                                    printf("\n > Sudoku incorreto.");
                                    return 0;
                                }
                            }
                        }
                    }
                }
                else
                {
                    printf("\n");
                    printf(" --------------------------------------\n");
                    printf(" *     >>  OBRIGADO POR JOGAR  <<     *\n");
                    printf(" --------------------------------------\n\n");
                    return 0;
                }
            }
            if (continuarJogando == 's' || continuarJogando == 'S')
            {
                break;
            }
            else
            {
                printf("\n > Entrada invalida. Tente novamente.");
                continue;
            }
        } while (continuarJogando != 's' && continuarJogando != 'S');

    } while (continuarJogando == 's' || continuarJogando == 'S');
}

// Função para exibir o menu e obter a escolha do usuário
int menu(char *nome)
{
    int escolha = 0;

    printf(" --------------------------------------\n");
    printf(" ---------------- Menu ----------------\n");
    printf(" *                                    *\n");
    printf(" *       1. Novo jogo                 *\n");
    printf(" *       2. Escolher jogo             *\n");
    printf(" *       3. Ranking                   *\n");
    printf(" *       4. Sair                      *\n");
    printf(" *                                    *\n");
    printf(" --------------------------------------\n\n");
    printf(" -> ");
    scanf("%d", &escolha);
    printf("\n");

    return escolha;
}

// Função para escolher um jogo
void escolherJogo(int grid[SIZE][SIZE])
{
    char nomearquivo[300];
    FILE *file;
    scanf("%*c");
    while (1) {
        printf("\nEntre com o nome do arquivo onde está seu sudoku:\n");
        fgets(nomearquivo, sizeof(nomearquivo), stdin);
        nomearquivo[strcspn(nomearquivo, "\n")] = '\0';
        file = fopen(nomearquivo, "r");
        if (file != NULL) {
            break;
        }
        printf("\nArquivo não existe ou não pôde ser aberto, tente novamente.\n");
    }

    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            if (fscanf(file, "%d", &grid[i][j]) != 1) {
                fprintf(stderr, "Erro ao ler dados da matriz no arquivo '%s'.\n", nomearquivo);
                fclose(file);
                exit(EXIT_FAILURE);
            }
        }
    }

    fclose(file);
}

// Função para mostrar ranking
void mostrarRanking()
{
    FILE *file = fopen("records.txt", "r");
    if (file == NULL)
    {
        printf("\n > Não foi possível abrir o arquivo de records.");
        return;
    }

    char nome[100][100];
    int tempo[100], cont = 0;

    while (fscanf(file, "%s %d", nome[cont], &tempo[cont]) != EOF)
    {
        cont++;
    }

    // Ordena os tempos
    for (int i = 0; i < cont - 1; i++)
    {
        for (int j = 0; j < cont - i - 1; j++)
        {
            if (tempo[j] > tempo[j + 1])
            {
                // Troca os tempo
                int temp = tempo[j];
                tempo[j] = tempo[j + 1];
                tempo[j + 1] = temp;

                // Troca os nome correspondentes
                char tempNome[100];
                strcpy(tempNome, nome[j]);
                strcpy(nome[j], nome[j + 1]);
                strcpy(nome[j + 1], tempNome);
            }
        }
    }

    // Exibe o ranking ordenado
    printf("\n --------------------------------------");
    printf("\n *         Ranking atual              *");
    printf("\n --------------------------------------");

    if (cont == 0)
    { // Verifica se o arquivo está vazio
        printf("\n | > Jogue uma partida e inicie o ranking!");
    }
    else
    {
        for (int n = 0; n < 3 && n < cont; n++)
        {
            printf("\n | > %d. %s - %d segundos", n + 1, nome[n], tempo[n]);
        }
    }
    printf("\n --------------------------------------");
}
// Função para atualizar e salvar records
void records(char *nome, int tempo)
{
    FILE *file = fopen("records.txt", "a");
    if (file == NULL)
    {
        printf("\n Não foi possível abrir o arquivo de records.\n");
        return;
    }

    fprintf(file, "%s %d\n", nome, tempo);
    fclose(file);
}

int main()
{
    int dif = 0, opcaoMenu = 0;
    int grid[SIZE][SIZE];
    int cont = 0;
    srand(time(0)); // Inicializar o gerador de números aleatórios
    char nick[NICK_SIZE];
    char nomeExistente[NICK_SIZE];
    int nomeEncontrado = 0;

   FILE *nome = fopen("nome.txt", "r+"); // Abre o arquivo para leitura e escrita
    if (nome == NULL) {
        printf("\n > Erro ao abrir o arquivo.\n");
        exit(1);
    }

    while (1) { 
        printf("\n");
        printf(" -----------------------------------------\n");
        printf(" *                                       *\n");
        printf(" *            Insira seu nick            *\n");
        printf(" *                                       *\n");
        printf(" -----------------------------------------\n");
        printf("\n-> ");
        scanf(" %s", nick);

        nomeEncontrado = 0; 
        rewind(nome);

        
        while (fscanf(nome, "%s", nomeExistente) != EOF) {
            if (strcmp(nomeExistente, nick) == 0) {
                nomeEncontrado = 1;
                break; 
            }
        }

        if (nomeEncontrado) {
            printf("\n > O nick %s ja existe no arquivo. Tente novamente.\n", nick);
        } else {
            printf("\n > Ola %s!", nick);
            fclose(nome);
            break; 
        }
    }
    
    printf("\n");
    while (opcaoMenu != 4)
    {
        opcaoMenu = menu(nick);

        if (opcaoMenu == 1)
        {
            dif = dificuldade();
            gerarSudoku(grid);
            level(dif, grid);
            clock_t start_time = clock();
            jogar(grid);

            int verificar = verificarSudoku(grid);
            if (verificar == 1)
            {
                clock_t end_time = clock();
                int tempo = (int)(end_time - start_time) / CLOCKS_PER_SEC;
                printf("\n > Seu tempo: %d segundos\n", tempo);
                records(nick, tempo);
            }
        }
        else if (opcaoMenu == 2)
        {
            escolherJogo(grid);
            dif = dificuldade();
            level(dif, grid);
            clock_t start_time = clock();
            jogar(grid);

            int verificar = verificarSudoku(grid);
            if (verificar == 1)
            {
                clock_t end_time = clock();
                int tempo = (int)(end_time - start_time) / CLOCKS_PER_SEC;
                printf("\n > Seu tempo: %d segundos\n", tempo);
                records(nick, tempo);
            }
        }
        else if (opcaoMenu == 3)
        {
            mostrarRanking();
        }
        else if (opcaoMenu == 4)
        {
            printf(" --------------------------------------\n");
            printf(" *     >>  OBRIGADO POR JOGAR  <<     *\n");
            printf(" --------------------------------------\n");
        }
        else
        {
            printf(" --------------------------------------\n");
            printf(" *           >> ERRO 404 <<           *\n\n");
            printf(" --------------------------------------\n");
        }
    }

    return 0;
}