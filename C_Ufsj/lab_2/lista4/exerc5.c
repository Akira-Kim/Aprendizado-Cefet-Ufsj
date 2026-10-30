#include<stdio.h>
#include<stdlib.h>

int main(){
    int a, b=0, x;

    printf("EScreva o salario pra saber o valor da taxa\n");
    scanf("%d", &a);

    if(a<=600){
        printf("Ate 600 é isento.");
    }
    if(a>=601 && a<=1300){
        x=(a-600)*(10/100);
        b=x;
        printf("O valor da taxa é de %d", b);
    }
    else if(a>=1301){
        x=(a-1300)*0.15;
        b=70+x;
        printf("O valor da taxa é de %d\n", x);
        printf("O valor total é de %d", b);

    }

return 0;

}