// geracao.dart

import 'package:flutter/material.dart';

import 'package:prova/generation_model.dart'; // Importe o modelo de dados

class GenerationItem extends StatelessWidget {
  final Generation generation;
  final void Function() onTap;

  GenerationItem({
    required this.generation,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: Text(generation.title),
      onTap: onTap,
    );
  }
}
