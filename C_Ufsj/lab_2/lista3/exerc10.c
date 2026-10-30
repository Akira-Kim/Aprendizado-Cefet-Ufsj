#include<stdio.h>
#include<stdlib.h>
int main(){

    float x, y, p ,r;

    printf("Digite o valor do salario e qual porcentaagem de almento\n");
    scanf("%f", &x);
    scanf("%f", &y);
    p=y/100;
    r=x*p;
    printf("%.1f", r+x);


    return 0;
}