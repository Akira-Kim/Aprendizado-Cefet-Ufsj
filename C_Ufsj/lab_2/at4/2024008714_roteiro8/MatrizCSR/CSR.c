#include "CSR.h"
#include <stdio.h>
#include <stdlib.h>
#define MAXL 5
#define MAXC 5

void criaMatriz(Matriz *m){
    m->data = (int*) malloc (sizeof(int) * MAXC * MAXL);
    m->jc = (int*) malloc (sizeof(int) * MAXC * MAXL);
    m->jr = (int*) malloc (sizeof(int) * MAXL + 1);
    m->Nz = 0;
    m->l = MAXL;
    m->c = MAXC;
}

void apagaMatriz(Matriz *m){
    free(m->data);
    free(m->jc);
    free(m->jr);
}

void alteraElementoNaMatriz(Matriz *m, int lin, int col, int valor) {
    if (valor == 0) {
        for (int i = m->jc[lin]; i < m->jc[lin + 1]; i++) {
            if (m->jr[i] == col) {
                for (int j = i; j < m->Nz - 1; j++) {
                    m->data[j] = m->data[j + 1];
                    m->jr[j] = m->jr[j + 1];
                }
                m->Nz--;
                break;
            }
        }
    } else {
        for (int i = m->jc[lin]; i < m->jc[lin + 1]; i++) {
            if (m->jr[i] == col) {
                m->data[i] = valor;  
                return;
            }
        }

        m->data[m->Nz] = valor;
        m->jr[m->Nz] = col;
        m->jc[lin + 1] = m->jc[lin + 1] + 1; 
        m->Nz++;
    }
}

int consultaElementoNaMatriz(Matriz *m, int lin, int col) {
    for (int i = m->jc[lin]; i < m->jc[lin + 1]; i++) {
        if (m->jr[i] == col) {
            return m->data[i]; 
        }
    }
    return 0;
}

void imprimeMatriz(Matriz *m) {
    for (int i = 0; i < m->l; i++) {
        for (int j = 0; j < m->c; j++) {
            int ver = 0;
            for (int k = m->jc[i]; k < m->jc[i + 1]; k++) {
                if (m->jr[k] == j) {
                    printf("%d ", m->data[k]);
                    ver = 1;
                    break;
                }
            }
            if (!ver) {
                printf("0 ");
            }
        }
        printf("\n");
    }
    printf("----------------------------------------------\n");
}

Matriz* getTransporta(Matriz *m){
    Matriz* m2;
    criaMatriz(m2);
    for (int i = 0; i <= m->c; i++) {
        m2->jc[i] = 0;
    }

    for (int i = 0; i < m->Nz; i++) {
        m2->jc[m->jr[i] + 1]++;
    }

    for (int i = 1; i <= m->c; i++) {
        m2->jc[i] += m2->jc[i - 1];
    }

    for (int i = 0; i < m->l; i++) {
        for (int j = m->jc[i]; j < m->jc[i + 1]; j++) {
            int lin = m->jr[j];
            int col = i;
            m2->data[m2->jc[lin]] = m->data[j];
            m2->jr[m2->jc[lin]] = col;
            m2->jc[lin]++;
        }
    }

    return m2;
}

Matriz* somaMatrizes(Matriz *m1, Matriz *m2){
    Matriz* m3;
    criaMatriz(m3);
     for (int i = 0; i <= m1->l; i++) {
        m3->jc[i] = 0;
    }

    for (int i = 0; i < m1->Nz; i++) {
        m3->jc[m1->jr[i] + 1]++;
    }

    for (int i = 0; i < m2->Nz; i++) {
        m3->jc[m2->jr[i] + 1]++;
    }

    for (int i = 1; i <= m1->l; i++) {
        m3->jc[i] += m3->jc[i - 1];
    }

    for (int i = 0; i < m1->l; i++) {
        int idx1 = m1->jc[i];
        int idx2 = m2->jc[i];

        while (idx1 < m1->jc[i + 1] && idx2 < m2->jc[i + 1]) {
            if (m1->jr[idx1] == m2->jr[idx2]) {
                m3->data[m3->Nz] = m1->data[idx1] + m2->data[idx2];
                m3->jr[m3->Nz] = m1->jr[idx1];
                m3->Nz++;
                idx1++;
                idx2++;
            } else if (m1->jr[idx1] < m2->jr[idx2]) {
                m3->data[m3->Nz] = m1->data[idx1];
                m3->jr[m3->Nz] = m1->jr[idx1];
                m3->Nz++;
                idx1++;
            } else {
                m3->data[m3->Nz] = m2->data[idx2];
                m3->jr[m3->Nz] = m2->jr[idx2];
                m3->Nz++;
                idx2++;
            }
        }
    }

    return m3;
}
