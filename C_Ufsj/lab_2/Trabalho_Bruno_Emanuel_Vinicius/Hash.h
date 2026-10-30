/*Implementado por:
    Bruno Rabelo de Andrade Mateus - 2024009972 
    Emanuel Felicio de Almeida - 2023020886
    Vinicius Duarte de Carvalho - 19000913
*/

#ifndef HASH_H
#define HASH_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ABP.h"
#define tam_max 26
typedef struct{
    ABP *tabela[tam_max];
    int tam, qtd;
}Hash;


Hash* criaHash(){
    Hash* h;
    h = (Hash*) malloc (sizeof(Hash));
    if(h != NULL){
        h->tam = tam_max; h->qtd = 0;
        if(h->tabela == NULL) return NULL;
        int i;
        for(i = 0; i<tam_max; i++)
            h->tabela[i] = criaABP();
    }
    return h;
}


void destroiHash(Hash *h){
    if(h != NULL){
        int i;
        for(i = 0; i<h->tam; i++)
            if(h->tabela[i] != NULL)
                destroiABP(h->tabela[i]);
        free(h);
    }
}

int insereHash_semTratar(Hash* h, char *v, int x){
    if(h == NULL) return 0;
    int pos = v[0] - 'a';
    insereElem(h->tabela[pos], v, x);
    return 1;
}

int buscaHash_semTratar(Hash* h, char *v){
    if(h == NULL) return 0;
    int pos = v[0] - 'a';
    return pesquisa(h->tabela[pos], v);;
}

#endif