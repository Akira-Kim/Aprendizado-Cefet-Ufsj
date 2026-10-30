#include <stdio.h>
#include <stdlib.h>

void repetir(char a, int b){

    int i;

    for (i = 1; i <= b; i++){
        if (i != b){
            printf("%c,", a);
        }
        else{
            printf("%c.", a);
        }
    }
}

int main(){

    int b, i;
    char a;

    printf("Escreva um caracter:");
    scanf("%c", &a);
    printf("\nEscreva quantas vezes quer repetir:");
    scanf("%d", &b);
    printf("\n\n");

    repetir(a, b);

    return 0;
}