#include <stdio.h>
#include <stdlib.h>

int mdc (int x, int y){
    int menor;
    if(x>y){
        menor=y;
    }else{
        menor=x;
    }
    int MDC=1;
    for(int i=1; i<=menor; i++){
        if(x%i==0 && y%i==0){
            MDC=i;
        }
    }
    return MDC;
}

float mmc (int x, int y){

    return (x*y)/mdc(x,y);

}

int main (){
    int x,y,MMC;
    scanf("%d %d",&x,&y);
    MMC=mmc(x,y);
    printf("%d\n",MMC);
    return 0;

}


