#include "listaprioridade.h"
#include <stdio.h>
#include <stdlib.h>

int main()
{

    ListaPrioridade fila;
    Pessoa p1, p2, p3, p4, p5;

    criaLista(&fila, 10);

    scanf("%d", &p1.prioridade);
    scanf("%s", p1.nome);
    insereNovaPessoaNoFinal(&fila, p1);

    scanf("%d", &p2.prioridade);
    scanf("%s", p2.nome);
    insereNovaPessoaNoFinal(&fila, p2);

    scanf("%d", &p3.prioridade);
    scanf("%s",p3.nome);
    insereNovaPessoaNoFinal(&fila, p3);

    scanf("%d", &p4.prioridade);
    scanf("%s", p4.nome);
    insereNovaPessoaNoFinal(&fila, p4);

    scanf("%d", &p5.prioridade);
    scanf("%s", p5.nome);
    insereNovaPessoaNoFinal(&fila, p5);

    imprimeLista(&fila);
    chamaProximaPessoa(&fila);

    imprimeLista(&fila);
    chamaProximaPessoa(&fila);

    imprimeLista(&fila);
    chamaProximaPessoa(&fila);

    imprimeLista(&fila);
    chamaProximaPessoa(&fila);

    imprimeLista(&fila);
    chamaProximaPessoa(&fila);

    imprimeLista(&fila);
    chamaProximaPessoa(&fila);
}