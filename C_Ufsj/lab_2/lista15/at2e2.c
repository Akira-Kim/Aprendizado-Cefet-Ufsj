#include <stdio.h>
#include <stdlib.h>

int main() { 
  int *x = (int*)malloc(sizeof(char)); 
  *x = 5; 
  free(x); 
  return 0;
} 
