

import 'package:aulas_navegacao/models/categorias.dart';
import 'package:flutter/material.dart';


class TelaProdutos extends StatelessWidget {

  //feito depois de criar a tela dos produtos
  final Categoria categoria; 

  const TelaProdutos(this.categoria);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Produtos"),
      ),
      body: Center(
        //child: Text("Produtos por Categoria")
        child: Text(this.categoria.titulo)
      ),
    );
  }
}