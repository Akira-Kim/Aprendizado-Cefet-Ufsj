#include <stdio.h>
#include <stdlib.h>

int main()
{

    int f = 1, s = 0, i = 0, m1, m2 = 99999999, ni = 0;
    float p;

    while (f != 0)
    {

        printf("\n ________________________________________________");

        printf("\n*Escreva um numero:");

        scanf("%d", &f);
        printf("                          *");

        if (f != 0)
        {

            s = s + f;
            printf("\n* soma: %d                                      *", s);

            i++;
            printf("\n* quantidade: %d                                *", i);

            if (f > m1)
            {

                m1 = f;
            }
            printf("\n* Maior numero: %d                              *", m1);

            if (f < m2)
            {

                m2 = f;
            }
            printf("\n* menor numero: %d                              *", m2);

            if (f % 2 != 0)
            {

                ni++;
            }
            p = (ni * 100) / i;
            printf("\n* porcentagem de numeros impares: %f         *", p);
        }
    }

    return 0;
}