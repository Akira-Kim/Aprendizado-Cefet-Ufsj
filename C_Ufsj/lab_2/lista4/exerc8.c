#include<stdio.h>
#include<stdlib.h>
int main(){
    float a, p;

    printf("Digite sua altura e peso:\n");
    scanf("%f ", &a);
    scanf("%f", &p);

    if(a<1.20){
        if(p<60){
            printf("A");
        }
        else if(p>=60 && p<=90){
            printf("D");
        }
        else if(p>90){
            printf("G");
        }
    }
    else if(a<=1.20 && a<=1.70){
        if(p<60){
            printf("B");
        }
        else if(p>=60 && p<=90){
            printf("E");
        }
        else if(p>90){
            printf("H");
        }
    }
    else if(a>1.70){
        if(p<60){
            printf("C");
        }
        else if(p>=60 && p<=90){
            printf("F");
        }
        else if(p>90){
            printf("I");
        }
    }


    return 0;
}