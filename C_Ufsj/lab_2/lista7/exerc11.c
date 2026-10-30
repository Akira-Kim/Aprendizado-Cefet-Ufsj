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

int main(){
    int x,y,mp;
    scanf("%d %d",&x,&y);
    mp=maior_primo(x,y);
    printf("%i\n",mp);
    return 0;
}

