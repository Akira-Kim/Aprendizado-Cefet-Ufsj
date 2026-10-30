#include<stdio.h>
#include<stdlib.h>
#include<math.h>

int main(){

    float x, y, r;

    printf("Digite largura e a altura de um retangulo:\n");
    scanf("%f", &x);
    scanf("%f", &y);

    r=x*y;

    printf("%2.f\n", r);

    return 0;
    
}