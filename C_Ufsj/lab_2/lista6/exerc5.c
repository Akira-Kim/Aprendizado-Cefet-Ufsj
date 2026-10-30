#include <stdio.h>
#include <stdlib.h>

int main()
{

    int ent = 0;

    while (ent != 4)
    {

        printf("mínimo múltiplo comum (MMC) entre a e b (opção 1)\nO máximo divisor comum (MDC) entre a e b (opção 2)");
        printf("\nO maior número primo que divide ambos (opção 3)\nSaída (opção 4)\n");
        scanf("%d", &ent);
        if (ent == 1)
        {
            int a, b, ac, bc, r;
            scanf("%d %d", &a, &b);
            ac = a;
            bc = b;
            while (b != 0)
            {
                int temp = b;
                b = a % b;
                a = temp;
            }
            r = (ac * bc) / a;

            printf("\nO mmc de %d e %d é: %d\n", ac, bc, r);
        }
        else if (ent == 2)
        {
            int a, b, ac, bc;
            scanf("%d %d", &a, &b);
            ac = a;
            bc = b;
            while (b != 0)
            {
                int temp = b;
                b = a % b;
                a = temp;
            }
            printf("\nO mdc de %d e %d é: %d\n", ac, bc, a);
        }
        else if (ent == 3)
        {
            int num1, num2;

            scanf("%d", &num1);

            scanf("%d", &num2);

            int a = num1, b = num2;
            while (b != 0)
            {
                int temp = b;
                b = a % b;
                a = temp;
            }
            int mdc = a;

            int maior_primo = 1;
            int n = mdc;

            while (n % 2 == 0)
            {
                maior_primo = 2;
                n /= 2;
            }

            for (int i = 3; i * i <= n; i += 2)
            {
                while (n % i == 0)
                {
                    maior_primo = i;
                    n /= i;
                }
            }

            if (n > 2)
            {
                maior_primo = n;
            }

            printf("O maior número primo que divide %d e %d é %d.\n", num1, num2, maior_primo);
        }
    }

    return 0;
}