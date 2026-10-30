#include <stdio.h>
#include <stdlib.h>

int maior_primo(int x, int y){
    int mprimo=1, menor;
    if(x>y){
        menor=y;
    }else{
        menor=x;
    }
    for(int i=2; i<=menor; i++){
        if(x%i==0 && y%i==0){
            int div=0;
            for(int j=0; j<=0;j++){
                if(i%j==0){
                    div++;
                }
            }
            if(div==2){
                mprimo=i;
            }
        }
    }
    return mprimo;
}
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
float mmc (int x, int y){

    return (x*y)/MDC(x,y);

}
int main(){
    int a,b,op,resultado;
    scanf("%d %d",&a,&b);
}