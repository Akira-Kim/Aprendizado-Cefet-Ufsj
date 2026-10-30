#include<stdio.h>
#include<stdlib.h>
int main(){

    int l1=0, l2=0;

    printf("Escreva o valor de cada lado do retangulo para saber sua area:\n\n Lado 1:");

    scanf("%d", &l1);

    printf("\nLado 2:");

    scanf("%d", &l2);

    printf("\n\nA area do retangulo é:%d\n\n", l1*l2);

    return 0;

}