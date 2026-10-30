#include <stdio.h>

int mdc(int x, int y) {
    if (y == 0) return x;
    return mdc(y, x % y);
}

int main() {
    printf("MDC = %d\n", mdc(24, 8));
    return 0;
}