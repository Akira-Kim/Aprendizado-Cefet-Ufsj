#include<stdio.h>
#include<stdlib.h>
#include<string.h>

int soma_algarismos(int x){
    if (x <=0){
        return -1;
    }
    char *v=malloc(sizeof(char)*12);
    sprintf(v, "%d", x);
    int size = strlen(v);
    int soma = 0;
    for (int i = 0; i < size; i++){
        soma+= v[i] - '0';
    }
    free(v);
    return soma;
}
int main (){
    int num;
    printf("\nDigite um numero: ");
    scanf("%i", &num);
    int resultado = soma_algarismos(num);
    if(resultado!= -1) {
        printf("\nSoma dos algarismos = %d\n", resultado);
    }else {
        printf("\n Numero invalido");
    }
    return 0;
}