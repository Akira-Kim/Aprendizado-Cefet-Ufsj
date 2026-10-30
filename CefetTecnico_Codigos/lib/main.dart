import 'package:flutter/material.dart';

import 'generations.dart';
import 'tela_geracoes.dart'; // Importe a tela de gerações

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Pokémon Generations',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        backgroundColor: Colors.grey[200], // Defina a cor de fundo desejada aqui
      ),
      home: GenerationsScreen(
        generations: generations, // Use a lista de gerações do seu modelo
      ),
    );
  }
}
