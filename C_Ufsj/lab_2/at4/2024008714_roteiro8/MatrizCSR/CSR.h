#ifndef CSR_H
#define CSR_H

typedef struct {
    int l, c; //quantidade de linhas e colunas da matriz
    int *data; //dados da matriz
    int *jr; //índice das colunas dos elementos
    int *jc; //Índice do começo das linhas
    int Nz; //quantidade de elementos não nulos na matriz
} Matriz;

void criaMatriz(Matriz *m);

void apagaMatriz(Matriz *m);

void alteraElementoNaMatriz(Matriz *m, int lin, int col, int valor);
 
int consultaElementoNaMatriz(Matriz *m, int lin, int col);

void imprimeMatriz(Matriz *m);

Matriz* getTransporta(Matriz *m);

Matriz* somaMatrizes(Matriz *m1, Matriz *m2);

#endif