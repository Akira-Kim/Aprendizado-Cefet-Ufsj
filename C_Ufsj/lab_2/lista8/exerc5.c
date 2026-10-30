#include <stdio.h>
#include <stdlib.h>

typedef struct { 
    float comp; 
    float lar;
    float h; 
} Caixa;

typedef struct {
    Caixa caixa1;
    Caixa caixa2;
    Caixa caixa3;
} Embalagem;

int podeCaber(Caixa a, Caixa b) {
    
    float a_dimensoes[3] = {a.comp, a.lar, a.h};
    float b_dimensoes[3] = {b.comp, b.lar, b.h};
    
    for (int i = 0; i < 3; i++) {
        for (int j = i + 1; j < 3; j++) {
            if (a_dimensoes[i] > a_dimensoes[j]) {
                float temp = a_dimensoes[i];
                a_dimensoes[i] = a_dimensoes[j];
                a_dimensoes[j] = temp;
            }
        }
    }
    
    for (int i = 0; i < 3; i++) {
        for (int j = i + 1; j < 3; j++) {
            if (b_dimensoes[i] > b_dimensoes[j]) {
                float temp = b_dimensoes[i];
                b_dimensoes[i] = b_dimensoes[j];
                b_dimensoes[j] = temp;
            }
        }
    }
    
   
    if (a_dimensoes[0] <= b_dimensoes[0] && a_dimensoes[1] <= b_dimensoes[1] && a_dimensoes[2] <= b_dimensoes[2]) {
        return 1; 
    }
    
    return 0; 
}

int cabe(Caixa a, Caixa b) {
    return podeCaber(a, b);
}

int main() {
    Embalagem embalagem;
   
    printf("Entre com as dimensões da caixa 1 (comp lar h): ");
    scanf("%f %f %f", &embalagem.caixa1.comp, &embalagem.caixa1.lar, &embalagem.caixa1.h);
    
    printf("Entre com as dimensões da caixa 2 (comp lar h): ");
    scanf("%f %f %f", &embalagem.caixa2.comp, &embalagem.caixa2.lar, &embalagem.caixa2.h);
    
    printf("Entre com as dimensões da caixa 3 (comp lar h): ");
    scanf("%f %f %f", &embalagem.caixa3.comp, &embalagem.caixa3.lar, &embalagem.caixa3.h);
    
    // Verificar se é possível colocar uma caixa dentro da outra
    if (cabe(embalagem.caixa1, embalagem.caixa2) && cabe(embalagem.caixa2, embalagem.caixa3)) {
        printf("Sim, é possível colocar as caixas uma dentro da outra.\n");
    } else {
        printf("Não, não é possível colocar as caixas uma dentro da outra.\n");
    }
    
    return 0;
}