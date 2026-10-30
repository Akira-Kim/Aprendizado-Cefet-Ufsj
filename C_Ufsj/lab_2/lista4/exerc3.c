#include<stdio.h>
#include<stdlib.h>

int main(){

    int a;


    printf("Escreva um nuemro de 1 a 12 para saber o mes\n");
    scanf("%d",&a);
    switch (a)
    {
    case 1:
        printf("janeiro");
        break;
    
    case 2:
        printf("Fevereiro");
        break;
    
    case 3:
        printf("Março");
        break;
    
    case 4:
        printf("Abril");
        break;
    
    case 5:
        printf("Maio");
        break;
    
    case 6:
        printf("Junho");
        break;
    
    case 7:
        printf("Julho");
        break;

    case 8:
        printf("Agosto");
        break;
    
    case 9:
        printf("Setembro");
        break;
    
    case 10:
        printf("Outubro");
        break;
    
    case 11:
        printf("Novembro");
        break;
    
    case 12:
        printf("Dezembro");
        break;
    
    
    default:
    printf("Não existe um mes com esse numero");
        break;
    }

    return 0;
}
