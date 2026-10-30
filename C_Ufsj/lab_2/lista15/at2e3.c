#include <stdio.h>
#include <stdlib.h>

int main() { 
  (int*)malloc(sizeof(int)); 
  int *x = 5; 
  free(x); 
  return 0;
} 

