#include <stdlib.h>
#include <stdio.h>

struct filme
{
    int id;
    int ano;
    int duracao_do_filme;

}typedef Filme;


int main(){

    Filme a;

    scanf("%d %d %d",&a.id,&a.ano,&a.duracao_do_filme);

    printf("%d %d %d",a.id,a.ano,a.duracao_do_filme);


    return 0;

}
