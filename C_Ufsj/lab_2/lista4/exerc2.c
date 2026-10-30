#include<stdio.h>
#include<stdlib.h>

int main(){

    int a, b;

    printf("Escreva dois numeros para saber o maior\n");
    scanf("%d", &a);
    scanf("%d", &b);

    if(a>b){
        printf("%d", a);
    }
    else if(a<b){
        printf("%d", b);
    }
    else{
        printf("Os numeros são iguais.");
    }
    

return 0;

}