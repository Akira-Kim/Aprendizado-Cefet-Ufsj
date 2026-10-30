#include<stdio.h>
#include<stdlib.h>
#include<math.h>

int main(){
    int b=0;
    float c, a, x;

    printf("EScreva o numero de lados e o tamanho do lado para saber a area e o formato da forma\n");
    scanf("%f", &a);
    scanf("%f", &c);

    if(a==3){
        
        x=2/(a*((sqrt(3)*a)/2));
        printf("triangulo %f\n",x);
    }
    else if(a==4){
        
        x=a*a;
        printf("quadrado %f\n", x);
    }
    else if(a==5){
        
        x=2/(5*(a*((sqrt(3)*a)/2)));
        printf("pentagono %f\n", x);
    }
    else{
        printf("Numero de lados invalido.");
    }


return 0;

}