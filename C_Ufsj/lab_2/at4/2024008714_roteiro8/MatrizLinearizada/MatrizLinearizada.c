#include "MatrizLinearizada.h"
#include <stdio.h>
#include <stdlib.h>
#define MAXL 10
#define MAXC 10

void criaMatriz(Matriz *m){
    m->data = (int*) malloc (sizeof(int)*MAXC*MAXL);
    m->l = 10;
    m->c = 10;
}

void apagaMatriz(Matriz *m){
    free(m->data);
}

void alteraElementoNaMatriz(Matriz *m, int lin, int col, int valor){
    m->data[lin *m->c + col] = valor;
}

int consultaElementoNaMatriz(Matriz *m, int lin, int col){
    return m->data[lin *m->c + col];
}

void imprimeMatriz(Matriz *m){
    for(int l = 0; l < MAXL; l++){
        for (int c = 0; c < MAXC; c++){
            printf("%d ", m->data[l * m->c + c]);
        }
        printf("\n");
    }
    printf("---------------------------------------------------\n");
}

Matriz* getTransporta(Matriz *m){
    Matriz* m2;
    criaMatriz(m2);
    for(int l = 0; l < MAXL; l++){
        for (int c = 0; c < MAXC; c++){
            m2->data[c * m->l + l] = m->data[l * m->c + c];
        }
    }
    return m2;
}

Matriz* somaMatrizes(Matriz *m1, Matriz *m2){
    Matriz* m3;
    criaMatriz(m3);
    int index;
    for (int l = 0; l < MAXL; l++){
        for (int c = 0; c < MAXC; c++){
            index = l * m3->c + c;
            m3->data[index] = m1->data[index] + m2->data[index];
        }
    }
    return m3;
}
