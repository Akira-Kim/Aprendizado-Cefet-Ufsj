#include<stdio.h>
#include<stdlib.h>
#include<math.h>
//o math nao funcionou vou compilar por outro lugar
struct coordenada{
   int x;
   int y;
};
struct Triangulo{
    struct coordenada p1;
    struct coordenada p2;
    struct coordenada p3;
};
float distancia(struct coordenada a, struct coordenada b) {
  return sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2));
}

void tipo_triangulo(struct Triangulo x) {
  float lado1 = distancia(x.p1, x.p2);
  float lado2 = distancia(x.p2, x.p3);
  float lado3 = distancia(x.p3, x.p1);

  if (lado1 == lado2 && lado2 == lado3) {
    printf("\no tringualo eh equilatero");
  } else if (lado1 == lado2 || lado1 == lado3 || lado2 == lado3) {
    printf("\n o tri eh isoceles");
  } else {
    printf("\n o tri eh escaleno");
  }
}

int main() {
  struct Triangulo tri;
  
  printf("\n insira as coordenadas: ");
  scanf("%d %d", &tri.p1.x, &tri.p1.y);
  printf("\n insira as coordenadas: ");
  scanf("%d %d", &tri.p2.x, &tri.p2.y);
  printf("\n insira as coordenadas: ");
  scanf("%d %d", &tri.p3.x, &tri.p3.y);

  tipo_triangulo(tri);

  return 0;
}