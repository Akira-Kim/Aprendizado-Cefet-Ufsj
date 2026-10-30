#include<stdio.h>
#include<stdlib.h>
int main(){

    int v1=0, v2=0, v3=0, r=0;

    printf("Digite 3 valores para saber a media:\n\nvalor 1:");

    scanf("%d", &v1);

    printf("\nvalor 2:");

    scanf("%d", &v2);
    
    printf("\nvalor 3:");

    scanf("%d", &v3);

    r=(v1+v2+v3)/3;

    printf("\n A media é:%d\n\n",r);

    return 0;
}