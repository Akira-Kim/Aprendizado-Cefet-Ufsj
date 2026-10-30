#include <stdio.h>
#include <stdlib.h>

float calcula(int n1, int n2, char simb)
{

    float r;

    if (simb == '+')
    {

        r = n1 + n2;
        return r;
    }
    else if (simb == '-')
    {

        r = n1 - n2;
        return r;
    }
    else if (simb == '*')
    {

        r = n1 * n2;
        return r;
    }
    else if (simb == '/')
    {

        r = n1 / n2;
        return r;
    }
    else
    {
        return -1;
    }
}

int main(){

    char simb;
    int n1, n2;
    float resultado;

    printf("Digite dois numeros e um simbulo das quatro operaçoes basicas");

    scanf("%d",&n1);
    scanf("%d",&n2);
    scanf("%c",&simb);

    resultado=calcula(n1,n2, simb);

    if(resultado==-1){

        exit(0);

    }

    printf("%f",resultado);

    return 0;
}