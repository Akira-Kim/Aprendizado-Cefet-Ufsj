/*Implementado por:
    Bruno Rabelo de Andrade Mateus - 2024009972 
    Emanuel Felicio de Almeida - 2023020886
    Vinicius Duarte de Carvalho - 19000913
*/

#include <stdio.h>
#include "Hash.h"

int main(){

    Hash* H;
    H = criaHash();

    char v[50];
    int n, valor;
    scanf("%d", &n);
    


    for (int i = 0; i < n; i++){
        scanf("%s", v);
        scanf("%d", &valor);
        insereHash_semTratar(H, v, valor);
    }

    getchar();
    int m;
    char u[50];

    scanf("%d", &m);
    printf ("Etapas de Busca:\n");
    
    for (int i = 0; i < m; i++){
        scanf("%s", u);
        getchar();
        int busca = buscaHash_semTratar(H, u);
        if(busca){
            printf("Palavra %s encontrada, valor: %d\n", u, busca);
        } else {
            printf("Palavra %s NÃO encontrada!\n", u);
        }
    }
    

    destroiHash(H);
    return 0;
}