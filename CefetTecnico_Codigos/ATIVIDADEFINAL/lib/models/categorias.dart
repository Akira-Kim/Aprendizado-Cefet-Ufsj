import 'package:flutter/material.dart';

class Categoria {
  final int id;
  final String titulo;
  final Color color;

  const Categoria ({
    required this.id,
    required this.titulo,
    this.color = Colors.orange,
  });

  // factory Categoria.fromJson(List<Map<String, dynamic>> json) {
  //   return json.map((e) => Categoria(id: e["id_categoria"], titulo: json["titulo"])) ;
  // }

}