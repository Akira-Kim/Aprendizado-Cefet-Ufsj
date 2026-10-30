int main()
{
    int limite = 2000;
    int soma = 0;
    int i;
    for (i = 0; i < limite; i += 2)
    {

        if (i % 3 == 0 || i % 5 == 0)
        {
            soma++;
        }
    }

    printf("A soma de todos os números pares abaixo de 2000 que são múltiplos de 3 ou 5 é: %d\n", soma);

    return 0;
}
