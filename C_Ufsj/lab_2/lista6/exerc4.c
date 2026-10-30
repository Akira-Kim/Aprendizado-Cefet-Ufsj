#include <stdio.h>
#include <stdlib.h>

int main()
{
    int x, y,r;

    scanf("%d %d", &x, &y);

    printf("    |");

    for (int i = x; i <= y; i++)
        {
            if(i<10){
                printf("  ");

            }

            printf("  %d",i);

        }

        printf(" \n--------------------------------------------------------------\n");


    for (int i = x; i <= y; i++)
    {


        printf(" %d  |", i);

        for (int j = x; j <= y; j++)
        {
            r=i * j;
            if(i<10){
                printf("  ");

            }

            printf("  %d", r);

        }
        printf("\n");
    }

    return 0;
}