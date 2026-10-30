#include "MatrizLinearizada.h"
#include <stdio.h>
#include <stdlib.h>

void preencheMatriz(Matriz* m){
    for (int l = 0; l < m->l; l++){
        for (int c = 0; c < m->c; c++){
            m->data[l * m->c + c] = rand() % 10;
        }
    }
}

int main(){
    Matriz m;
    criaMatriz(&m);
    preencheMatriz(&m);
    imprimeMatriz(&m);
    alteraElementoNaMatriz(&m, 2, 3, 10);
    printf("<%d>\n", consultaElementoNaMatriz(&m, 2, 3));
    Matriz mT;
    criaMatriz(&mT);
    mT = *getTransporta(&m);
    imprimeMatriz(&mT);
    Matriz soma;
    criaMatriz(&soma);
    soma = *somaMatrizes(&m, &mT);
    imprimeMatriz(&soma);
    apagaMatriz(&m);
    apagaMatriz(&mT);
    apagaMatriz(&soma);
}