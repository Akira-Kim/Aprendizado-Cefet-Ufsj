#include<stdio.h>

int main(){

    int a, b, c;

    scanf("%d %d %d", &a, &b, &c);

    if(a==b && a==c){

        printf("Equilatero");
    }else if(a!=b && a != c && b != c){

        printf("Escaleno");
    }else{

        printf("isosceles");
    }



    return 0;
}