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

  double r = pow((a+b),2);

  double s = pow((b+c),2);

  resultado = r+s/2;

  print(resultado);
  
}