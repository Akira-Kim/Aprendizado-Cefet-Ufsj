

import 'package:aulas_navegacao/Telas/tela_produtos.dart';
import 'package:flutter/material.dart';

import '../models/categorias.dart';
import '../utils/rotas.dart';

class CategoriaItem extends StatelessWidget {

  final Categoria categoria;

  CategoriaItem(this.categoria);

  void selecionarCategoria(BuildContext context){
    //PROGRAMAR
    // Navigator.of(context).push(
    //   MaterialPageRoute(builder: (_){
    //     return TelaProdutos(categoria);
    //   })
    // );
    

    Navigator.of(context).pushNamed(Rotas.PRODUTOS,  arguments: {'id': categoria.id, 'title': categoria.titulo});
  }
  
  @override
  Widget build(BuildContext context) {
    return  InkWell(
      onTap: () => selecionarCategoria(context),
      child: Container(
          padding: EdgeInsets.all(15),
          child: Text(categoria.titulo),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(15),
            gradient: LinearGradient(
            colors: [
              categoria.color.withOpacity(0.5),
              categoria.color
            ],
            begin: Alignment.topLeft,
            end : Alignment.bottomRight,
            )
          ),
        ),
    );
  
  }



}