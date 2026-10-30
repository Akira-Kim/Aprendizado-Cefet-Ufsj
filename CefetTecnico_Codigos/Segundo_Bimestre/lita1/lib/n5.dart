import 'dart:io';
import 'dart:math';

void main() {
  print("insira a?");

  double a = double.parse(stdin.readLineSync()!);

  double imposto = a + 28 / 100;

  double distribuidor = a + 45 / 100;

  double resultado = a + imposto + distribuidor;

  print(resultado);
}