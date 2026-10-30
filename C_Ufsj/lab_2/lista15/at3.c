#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* duplica_string(char str[]) {
    char *dup = (char *)malloc(strlen(str) + 1);
    strcpy(dup, str);
    return dup;
}

int main() {
    char original[] = "Hello";
    char *duplicada = duplica_string(original);
    printf("%s\n", duplicada);
    free(duplicada);
    return 0;
}