/*Implementado por:
    Bruno Rabelo de Andrade Mateus - 2024009972 
    Emanuel Felicio de Almeida - 2023020886
    Vinicius Duarte de Carvalho - 19000913
*/

#ifndef ABP_H
#define ABP_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct NO{
    struct NO* esq;
    struct NO* dir;
    char v[50];
    int n;
}NO;

typedef struct NO* ABP;
    


NO* alocarNO(){
    return (NO*) malloc (sizeof(NO));
}

void liberarNO(NO* q){
    free(q);
}

ABP* criaABP(){
    ABP* raiz = (ABP*) malloc (sizeof(ABP));
    if(raiz != NULL)
        *raiz = NULL;
    return raiz;
}

void destroiRec(NO* no){
    if(no == NULL) return;
    destroiRec(no->esq);
    destroiRec(no->dir);
    liberarNO(no);
    no = NULL;
}

void destroiABP(ABP* raiz){
    if(raiz != NULL){
        destroiRec(*raiz);
        free(raiz);
    }
}

int estaVazia(ABP* raiz){
    if(raiz == NULL) return 0;
    return (*raiz == NULL);
}


int insereRec(NO** raiz, char *v, int elem){
    if(*raiz == NULL){
        NO* novo = alocarNO();
        if(novo == NULL) return 0;
        novo->n = elem;
        strcpy(novo->v, v);
        novo->esq = NULL; novo->dir = NULL;
        *raiz = novo;
    }else{
        
        if(strcmp((*raiz)->v, v)> 0)
            return insereRec(&(*raiz)->esq, v, elem);
        else if(strcmp((*raiz)->v, v ) < 0)
            return insereRec(&(*raiz)->dir, v, elem);
    }
    return 1;
}

int insereElem(ABP* raiz, char *v,int elem){
    if(raiz == NULL) return 0;
    return insereRec(raiz, v, elem);
}

int pesquisaRec(NO** raiz, char *v){
    if(*raiz == NULL) return 0;
    if(strcmp((*raiz)->v, v) == 0) {
        return (*raiz)->n;
    } else if (strcmp((*raiz)->v, v) > 0){
         return pesquisaRec(&(*raiz)->esq, v);
    }else if (strcmp((*raiz)->v, v) < 0){
        return pesquisaRec(&(*raiz)->dir, v);
    }
}

   
int pesquisa(ABP* raiz, char *v){
    if(raiz == NULL) return 0;
    if(estaVazia(raiz)) return 0;
    return pesquisaRec(raiz, v);
}

#endif