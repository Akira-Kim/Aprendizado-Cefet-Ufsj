#include <stdlib.h>
#include <stdio.h>

struct n_complexo
{

    int n;
    int q;
    char l;

} typedef Comp;

Comp soma(Comp a, Comp b)
{

    Comp r;

    r.n = a.n + b.n;

    r.q = a.q + b.q;
    r.l = a.l;

    return r;
}

int main()
{

    Comp nc1, nc2, nc3;

    scanf("%d %d %c", &nc1.n, &nc1.q, &nc1.l);
    scanf("%d %d %c", &nc2.n, &nc2.q, &nc2.l);

    nc3 = soma(nc1, nc2);

    printf("%d + %d%c\n", nc3.n, nc3.q, nc3.l);

    return 0;
}
