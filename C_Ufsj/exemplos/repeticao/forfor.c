#include<stdio.h>
#include<stdlib.h>
int main(){

    float a, b, c=1;
    int i;

    scanf("%f %f", &a, &b);

    for(i=0;i!=b;i++){

        c=c*a;

    }
    printf("%f\n",c);


    return 0;
}