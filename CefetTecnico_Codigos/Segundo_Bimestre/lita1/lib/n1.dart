import 'dart:io';
import 'dart:math';

void main() {
  
    print("insira x1?");
  double x1 = double.parse(stdin.readLineSync());  

  print("insira x2?");
  double x2 = double.parse(stdin.readLineSync());  

  print("insira y1?");
  double y1 = double.parse(stdin.readLineSync());  

  print("insira y2?");
  double y2 = double.parse(stdin.readLineSync());  

  double resultado;

  resultado = pow((x2-x1),2) + pow((y2-y1),2);

  double fim = sqrt(resultado);

  print(resultado);
  
}