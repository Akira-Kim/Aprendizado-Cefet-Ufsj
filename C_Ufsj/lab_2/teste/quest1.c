int ehPrimo(int num)
{
    if (num <= 1)
        return 0;
    if (num <= 3)
        return 1;

    if (num % 2 == 0 || num % 3 == 0)
        return 0;

    for (int i = 5; i * i <= num; i += 6)
    {
        if (num % i == 0 || num % (i + 2) == 0)
            return 0;
    }

    return 1;
}

void imprimirDivisores(int n)
{
    for (int i = 1; i <= n; ++i)
    {
        printf("Divisores de %d: ", i);
        for (int j = 1; j <= i; ++j)
        {
            if (i % j == 0)
            {
                printf("%d ", j);
            }
        }
        if (ehPrimo(i))
        {
            printf("(Primo)");
        }
        printf("\n");
    }
}

int main()
{
    int N;

    printf("Digite um valor para N: ");
    scanf("%d", &N);

    imprimirDivisores(N);

    return 0;
}