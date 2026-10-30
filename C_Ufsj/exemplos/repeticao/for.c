#include<stdio.h>
#include<stdlib.h>
int main(){

    int i=3, x;

    scanf("%d",&x);

    while(x!=12345){
        i--;
        if(i==0){
            printf(" nuemro de tentativas maxima atingido");
            return 0;
        }
        scanf("%d", &x);
    }

    return 0;
}