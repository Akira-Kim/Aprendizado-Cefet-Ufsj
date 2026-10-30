#include <stdlib.h>
#include <stdio.h>

int main()
{

    int a, b, *c, *d;

    c = &a;
    d = &b;

    if (c > d)
    {
        printf("%p c\n\n", c);
    }
    else if (c < d)
    {
        printf("%p d\n\n", d);
    }

    return 0;
}