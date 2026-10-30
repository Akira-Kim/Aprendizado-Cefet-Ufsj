#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int MDC (int x, int y){

    int menor,mdc=1;
    if(x>y){
        menor=x;
    }else{
        menor=y;
    }
    for(int i=1;i<=menor;i++){

        if(x%i==0 && y%i==0){

            mdc=i;

        }

    }
    return mdc;

}

int main (){
    int x,y,mdc;
    scanf("%d %d",&x,&y);
    mdc=MDC(x,y);
    printf("%d\n",mdc);
    return 0;
}