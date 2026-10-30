#include<stdio.h>

int main(){

    int a;

    printf("Digite sua idade para saber sua categoria:\n\n");

    scanf("%d",&a);

    if(10<=a && a<=14){

        printf("infantil");


    }else if(a<=17){

        printf("Juvenil");


    }else if(a<=50){

        printf("Adulto");


    }else if(a>50){

        printf("Idoso");

    }
    
    return 0;
}
