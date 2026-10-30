import 'package:flutter/material.dart';

class Categoria {
  final int id;
  final String titulo;
  final Color color;

  const Categoria({
    required this.id,
    required this.titulo,
    this.color = Colors.orange,
  });
}
