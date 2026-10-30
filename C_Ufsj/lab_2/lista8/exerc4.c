#include <stdio.h>

typedef struct{ 
  float comprimento; 
  float largura;
  float altura; 
} Caixa;

int cabe(Caixa a, Caixa b){
  if (a.comprimento < b.comprimento && a.largura < b.largura && a.altura < b.altura){
    return 1;
  } else {
    return 0;
  }
}

int main() {
  Caixa caixaA, caixaB;

  printf("\ndimensoes caixa a (comprimento, largura, altura): ");
  scanf("%f %f %f", &caixaA.comprimento, &caixaA.largura, &caixaA.altura);

  printf("\ndimensoes da caixa b (comprimento, largura, altura): ");
  scanf("%f %f %f", &caixaB.comprimento, &caixaB.largura, &caixaB.altura);

  if (cabe(caixaA, caixaB)) {
    printf("a caixa A cabe dentro da caixa B.\n");
  } else {
    printf("a caixa A nao cabe dentro da caixa B.\n");
  }

  return 0;
}