#include<stdio.h>
#include<stdlib.h>
int main(){
    float a, p, x;

    printf("Digite sua altura e peso:\n");
    scanf("%f ", &a);
    scanf("%f", &p);

    x=p/(a*a);

    if(x<=18.5){
        printf("Abaixo do peso");
    }
    else if(x>=18.6 && x<=24.9){
        printf("Saudavel");
    }
    else if(x>=25 && x<=29.9){
        printf("Peso em exesso");
    }
    else if(x>=30 && x<=34.9){
        printf("Obesidade grau I");
    }
    else if(x>=35 && x<=39.9){
        printf("Obesidade grau II(severa)");
    }
    else if(x>40){
        printf("Obesidade grau III(Morbida)");
    }
     
    return 0;
}