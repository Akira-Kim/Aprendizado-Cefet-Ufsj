#include <stdio.h>
#include<stdlib.h>
#include <math.h>


//pedi para outra pessoa rodar o codigo
// por algum motivo em meu computador o math.h 
// não esta funcionando

struct coordenada
{
    float x;
    float y;
};

double distancia(struct coordenada ponto1, struct coordenada ponto2)
{

    double dist = pow(ponto2.x - ponto1.x, 2) + pow(ponto2.y - ponto1.y, 2);
    return sqrt(dist);
}

int main()
{
    struct coordenada ponto1, ponto2;

    printf("Quais as coordenadas do ponto 1 (x y): ");
    scanf("%f %f", &ponto1.x, &ponto1.y);

    printf("Quais as coordenadas do ponto 2 (x y): ");
    scanf("%f %f", &ponto2.x, &ponto2.y);

    double dist = distancia(ponto1, ponto2);
    printf("Distância euclidiana: %.2f\n", dist);

    return 0;
}