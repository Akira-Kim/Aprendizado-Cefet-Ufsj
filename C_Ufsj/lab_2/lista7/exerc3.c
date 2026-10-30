#include <stdio.h>
#include <stdlib.h>

float transsegundos(int h, int m, int s)
{

    int segundos=0;
    segundos += h * 60;
    segundos += m * 60;
    segundos += s;

    return segundos;
}

int main()
{

    int h, m, s, r;

    printf("Escreva horas, minutos e depois segundos: ");
    scanf("%d", &h);
    scanf("%d",&m);
    scanf("%d",&s);

    r = transsegundos(h, m, s);

    printf("\n\n______________________________________");
    printf("\ntempo em segundos: %d\n\n", r);

    return 0;
}