import 'dart:io';
import 'dart:math';

void main() {
  
    print("insira a?");
  double a = double.parse(stdin.readLineSync());  

  print("insira b?");
  double b = double.parse(stdin.readLineSync());  

  print("insira c?");
  double c = double.parse(stdin.readLineSync());  

  double resultado;

  double r = 2 * a;
    
  double s = 3 * b;

  double q = 5 *c;

  resultado = (r + s + q) / 3;

  print(resultado);
  
}