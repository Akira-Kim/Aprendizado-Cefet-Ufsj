#include <stdlib.h>
#include <stdio.h>

void muda_valores(int *p)
{

    p[4] = 100;
}

int soma_valores(int a[])
{

    int b = a[0] + a[1] + a[5];
    return b;
}

int main()
{

    int a[6] = {1, 0, 5, -2, -5, 7};

    int b = soma_valores(a);

    muda_valores(a);

    for (int i = 0; i < 6; i++)
    {

        printf("%d\n", a[i]);
    }

    return 0;
}