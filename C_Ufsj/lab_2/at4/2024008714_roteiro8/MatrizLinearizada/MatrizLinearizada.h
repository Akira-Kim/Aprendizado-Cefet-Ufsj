#ifndef MATRIZLINEARIZADA_H
#define MATRIZLINEARIZADA_H

typedef struct {
    int l, c; //linhas e colunas
    int *data; //dados da matriz
} Matriz;

void criaMatriz(Matriz *m);

void apagaMatriz(Matriz *m);

void alteraElementoNaMatriz(Matriz *m, int lin, int col, int valor);
 
int consultaElementoNaMatriz(Matriz *m, int lin, int col);

void imprimeMatriz(Matriz *m);

Matriz* getTransporta(Matriz *m);

Matriz* somaMatrizes(Matriz *m1, Matriz *m2);

#endif