#include <stdio.h>
#include <stdlib.h>

int main()
{
    char xadrez[8][8];
    int x, y;
    scanf("%d %d", &x, &y);
    printf("   ");
    for (int i = 0; i < 8; i++)
    {
        printf(" %d ",i+1);
        for (int j = 0; j < 8; j++)
        {
            xadrez[i][j] = '-';
        }
    }
    printf("\n--------------------------");
    for (int i = 0; i < 8; i++)
    {
        xadrez[i][y - 1] = 'x';
    }
    for (int i = 0; i < 8; i++)
    {
        xadrez[x - 1][i] = 'x';
    }
    printf("\n");
    for (int i = 0; i < 8; i++)
    {
        printf("%d |",i+1);
        for (int j = 0; j < 8; j++)
        {
            
            printf(" %c ", xadrez[i][j]);
        }
        printf("\n");
    }

    return 0;
}