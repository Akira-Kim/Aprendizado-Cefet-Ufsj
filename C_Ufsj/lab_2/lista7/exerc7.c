#include<stdio.h>
#include<stdlib.h>

char maiusculo(char x){
    if (x>= 97 && x <= 122){
        return x - 32;
    }else if(x >= 65 && x <= 90){
        return x;
    }else{
        printf("\nnao eh uma letra");
        return x;
    }
}

int main(){
    char x;
    printf("\n inserir vogal minuscula ");
    scanf("%c",&x);
    printf("\n%c\n", maiusculo(x));
    return 0;
}