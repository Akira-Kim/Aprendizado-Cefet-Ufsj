#include "listaprioridade.h"
#include <stdlib.h>
#include <stdio.h>

void criaLista(ListaPrioridade *lista, int tamanhoMaximo)
{

    lista->tamanhoMaximo = tamanhoMaximo;
    lista->pessoas = (Pessoa *)malloc(sizeof(Pessoa) * tamanhoMaximo);
    lista->primeiro = 0;
    lista->ultimo = -1;
}

int VerificaListaVazia(ListaPrioridade *lista)
{

    if (lista->ultimo == -1)
    {
        return 1;
    }
    return 0;
}

int insereNovaPessoaNoFinal(ListaPrioridade *lista, Pessoa pessoa)
{

    if (lista->ultimo == lista->tamanhoMaximo)
    {
        return 0;
    }

    lista->ultimo++;

    lista->pessoas[lista->ultimo] = pessoa;

    printf("%s adicionada com prioridade %d\n", lista->pessoas[lista->ultimo].nome, lista->pessoas[lista->ultimo].prioridade);

    return 1;
}

int chamaProximaPessoa(ListaPrioridade *lista)
{

    int indice = 0;
    int prioridade = 0;

    for (int i = 0; i <= lista->ultimo; i++)
    {

        if (lista->pessoas[i].prioridade > prioridade)
        {

            prioridade = lista->pessoas[i].prioridade;
            indice = i;
        }
    }

    printf("Proximo: %s, %d\n", lista->pessoas[indice].nome, prioridade);

    while (indice < lista->ultimo)
    {

        lista->pessoas[indice] = lista->pessoas[indice + 1];
        indice++;
    }

    lista->ultimo--;
}

int procura(ListaPrioridade lista, Prioridade x)
{

    for (int i = 0; i < lista.ultimo; i++)
    {

        if (lista.pessoas[i].prioridade == x)
        {

            return i;
        }
    }

    return -1;
}// complexidade o(n)

int quantosFaltam(ListaPrioridade Lista, Prioridade x)
{

    int cont = 0;

    for (int i = 0; i < Lista.ultimo; i++)
    {
        if (x <= Lista.pessoas[i].prioridade)
        {
            cont++;
        }
    }
    if (cont == 0)
    {
        return 0;
    }

    return cont - 1;
}// complexidade o(n)

void insertOrd(ListaPrioridade lista, Pessoa x)
{


    if (lista.ultimo == lista.tamanhoMaximo)
    {
        printf("lista cheia\nERRO\n");
        return 0;
    }

    int ind = 0;

    for (int i = 0; i < lista.ultimo; i++)
    {

        if (lista.pessoas[i].prioridade <= x.prioridade)
        {

            ind = i;
            break;
        }
    }
    if (ind == 0)
    {
        ind = lista.ultimo + 1;
        lista.ultimo++;
    }
    else
    {
        lista.ultimo++;

        for (int k = lista.ultimo; k > ind; k--)
        {
            lista.pessoas[k] = lista.pessoas[k-1];

        }

        lista.pessoas[ind] = x;
    }

    
} // complexidade o(n)

void imprimeLista(ListaPrioridade *lista)
{

    if (lista->ultimo == -1)
    {
        printf("Lista vazia\n");
    }
    else
    {

        for (int i = 0; i <= lista->ultimo; i++)
        {
            printf("%s, %d\n", lista->pessoas[i].nome, lista->pessoas[i].prioridade);
        }
    }
}