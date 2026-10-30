#include<stdio.h>

int main(){

    int x, y;

    scanf("%d %d", &x, &y);

    while (x<=y){
        if(x%2==0){
            printf("%d\n", x);
        }
        x++;
    }
    

    return 0;
}