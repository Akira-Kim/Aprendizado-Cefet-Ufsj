#include "CSR.h"
#include <stdio.h>
#include <stdlib.h>

void preencheMatriz(Matriz* m){
    alteraElementoNaMatriz(m, 2, 3, 10);
    alteraElementoNaMatriz(m, 2, 4, 9);
    alteraElementoNaMatriz(m, 3, 3, 7);
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
}