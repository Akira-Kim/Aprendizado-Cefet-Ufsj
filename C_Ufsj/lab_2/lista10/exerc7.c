#include <stdio.h>

struct Coordenada {
    float x;
    float y;
};

int existe_coordenada(struct Coordenada coordenadas[], int n, struct Coordenada coordenada) {
    for (int i = 0; i < n; i++) {
        if (coordenadas[i].x == coordenada.x && coordenadas[i].y == coordenada.y) {
            return 1;
        }
    }
    return 0;
}

int main() {
    int n;
    printf("Digite o número de coordenadas: ");
    scanf("%d", &n);

    struct Coordenada coordenadas[n];

    printf("Digite as coordenadas (x y) para cada ponto:\n");
    for (int i = 0; i < n; i++) {
        scanf("%f %f", &coordenadas[i].x, &coordenadas[i].y);
    }

    struct Coordenada coord_ref;
    printf("Digite a coordenada de referência (x y): ");
    scanf("%f %f", &coord_ref.x, &coord_ref.y);

    if (existe_coordenada(coordenadas, n, coord_ref)) {
        printf("A coordenada existe no vetor.\n");
    } else {
        printf("A coordenada não existe no vetor.\n");
    }

    return 0;
}