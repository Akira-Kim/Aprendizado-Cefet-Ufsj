#include<stdlib.h>
#include<stdio.h>

int main(int argc,char *argv[]){

    int cont=0;
    char l;

    FILE *arq = fopen(argv[1], "r");
    if(arq == NULL){
        printf("ERRO");
        return 0;
    }
    while ((l = fgetc(arq) != EOF)){

        if(l=='\n'){
            cont++;
        }
    }
    fclose(arq);
    printf("O numero de linhas é %d",cont);

    return 0;

}