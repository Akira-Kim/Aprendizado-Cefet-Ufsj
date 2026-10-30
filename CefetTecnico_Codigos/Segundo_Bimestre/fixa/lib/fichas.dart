import 'package:flutter/material.dart';
import 'dart:math';


class Ficha extends StatelessWidget {
  final String imageUrl;
  final String nome;
  final int matricula;
  final String escola;
  final String ano;
  final String periodo;

  Ficha({
    required this.imageUrl,
    required this.nome,
    required this.matricula,
    required this.escola,
    required this.ano,
    required this.periodo,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Column(
        children: [
          Image.network(
            imageUrl,
            width: 100,
            height: 150,
            fit: BoxFit.cover,
          ),
          SizedBox(height: 10),
          Text('Nome: $nome'),                 
          Text('Matrícula: $matricula'),
          Text('Escola: $escola'),
          Text('Ano: $ano'),
          Text('Período: $periodo')
        ],
      ),
    );
  }
}