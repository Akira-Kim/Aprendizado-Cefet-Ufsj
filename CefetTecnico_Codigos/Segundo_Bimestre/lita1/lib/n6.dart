import 'dart:io';
import 'dart:math';

void main() {
  
    print("insira a?");
  double a = double.parse(stdin.readLineSync()!);  

  print("insira b?");
  double b = double.parse(stdin.readLineSync()!);  

  print("insira c?");
  double c = double.parse(stdin.readLineSync()!);  

  print("insira d?");
  double d = double.parse(stdin.readLineSync()!);  

  print("insira e?");
  double e = double.parse(stdin.readLineSync()!);  

  print("insira f?");
  double f = double.parse(stdin.readLineSync()!);  


  double x = c*e-b*f/a*e-b*d;

  double y = a*f-c*d/a*e-b*d;


  print(x);

  print(y);
  
}
