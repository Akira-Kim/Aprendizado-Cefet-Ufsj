#include <stdio.h>

int menorElemento(int arr[], int n) {
    if (n == 1) return arr[0];
    int menor = menorElemento(arr, n - 1);
    return (arr[n - 1] < menor) ? arr[n - 1] : menor;
}

int main() {
    int arr[] = {5, 3, 8, 1, 4};
    int n = sizeof(arr) / sizeof(arr[0]);
    printf("Menor elemento: %d\n", menorElemento(arr, n));
    return 0;
}