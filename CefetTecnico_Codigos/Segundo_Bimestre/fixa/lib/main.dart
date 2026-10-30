import 'package:flutter/material.dart';
import 'dart:math';
import 'package:fixa/fichas.dart';




void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  final List<Ficha> fichas = [

    Ficha(
      imageUrl: 'https://png.pngtree.com/png-clipart/20230225/ourmid/pngtree-cartoon-fashion-future-technology-cyberpunk-game-movie-character-modeling-portrait-png-image_6619908.png',
      nome: 'James',
      matricula: Random().nextInt(99999),
      escola: 'CEFET-MG',
      ano: '2023',
      periodo: '2° Período',
    ),

    Ficha(
      imageUrl: 'https://png.pngtree.com/png-clipart/20230501/ourmid/pngtree-modern-styleof-cat-wearing-sunglasses-design-with-watercolor-splash-effect-png-image_6726317.png',
      nome: 'Júlia',
      matricula: Random().nextInt(99999),
      escola: 'CEFET-MG',
      ano: '2023',
      periodo: '3° Período',
    ),

    Ficha(
      imageUrl: 'https://png.pngtree.com/png-vector/20221207/ourmid/pngtree-luxury-life-and-rich-child-concept-png-image_6514130.png',
      nome: 'Fernando',
      matricula: Random().nextInt(99999),
      escola: 'CEFET-MG',
      ano: '2023',
      periodo: '6° Período',
    ),

        Ficha(
      imageUrl: 'https://png.pngtree.com/png-clipart/20230213/ourmid/pngtree-realistic-astronaut-illustration-png-image_6599323.png',
      nome: 'Sophia',
      matricula: Random().nextInt(99999),
      escola: 'CEFET-MG',
      ano: '2023',
      periodo: '3° Período',
    ),

        Ficha(
      imageUrl: 'https://png.pngtree.com/png-vector/20230201/ourmid/pngtree-cyber-bullying-and-online-crime-concept-png-image_6581175.png',
      nome: 'Akira',
      matricula: Random().nextInt(99999),
      escola: 'CEFET-MG',
      ano: '2023',
      periodo: '1° Período',
    ),

  ];

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Ficha de Alunos'),
        ),
        body: ListView.builder(
          itemCount: fichas.length,
          itemBuilder: (ctx, index) {
            return fichas[index];
          },
        ),
      ),
    );
  }
}

