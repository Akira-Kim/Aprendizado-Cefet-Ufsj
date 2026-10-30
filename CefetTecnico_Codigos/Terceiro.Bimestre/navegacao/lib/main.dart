import 'package:flutter/material.dart';
import 'package:navegacao/telas/tela_categorias.dart';
import 'package:navegacao/telas/tela_produtos.dart';
import 'package:navegacao/utils/rotas.dart';

void main() {
  runApp(MeuCardapio());
}

class MeuCardapio extends StatelessWidget {
  @override //subscrever metodo para criar elemento de widget
  Widget build(BuildContext context) {
    return MaterialApp(
        title: "Cardápio",
        theme: ThemeData(
          primaryColor: Colors.blue,
        ),
        //home: TelaCategorias(),
        routes: {
          Rotas.HOME: (ctx) => TelaCategorias(),
          Rotas.PRODUTOS: (ctx) => TelaProdutos()
        });
  }
}
