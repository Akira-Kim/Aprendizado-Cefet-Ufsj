import 'dart:io';
import 'dart:math';

void main() {
  
    print("insira a?");
  
  double segundos = double.parse(stdin.readLineSync());  

  double minutos =  segundos/60;

  double horas = minutos/60;

  print(horas);
  print(minutos);
  print(segundos);
  
  
}
