#include<stdio.h>
#include<stdlib.h>
int main(){

    int x,s,a;

    scanf("%d", &x);
    s=x+1;
    s=s*3;
    a=x-1;   
    a=a*2;
    x=a+s;
    printf("%d", x);




    return 0;
}