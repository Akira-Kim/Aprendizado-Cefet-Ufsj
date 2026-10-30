#include<stdio.h>
#include<stdlib.h>
int main(){
    int a, x;
    char b;


    printf("Digite a quilometragem da viagem e seu tipo de carro: A, B ou C. Para saber seu consumo.\n");
    scanf("%d ",&a);
    scanf("%c",&b);

    switch (b)
    {
    case 'A':
        x=12*a;
        printf("%d", x);
        break;

    case 'a':
        x=12*a;
        printf("%d", x);
        break;
    
    case 'B':
        x=9*a;
        printf("%d", x);
        break;
    
    case 'b':
        x=9*a;
        printf("%d", x);
        break;
    
    case 'C':
        x=8*a;
        printf("%d", x);
        break;
    
    case 'c':
        x=8*a;
        printf("%d", x);
        break;
    


    
    default:
        break;
    }

    return 0;
}