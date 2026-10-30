import 'package:flutter/material.dart';

import 'Telas/tela_categoria.dart';
import 'Telas/tela_produtos.dart';
import 'data/produtos.dart';
import 'models/produtos.dart';
import 'utils/rotas.dart';

void main() => runApp(AppCardapio());

class AppCardapio extends StatelessWidget {
  Future<List<dynamic>> teste = categoria_produtos();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Cardápio',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        fontFamily: 'Schyler',
        textTheme: ThemeData.light().textTheme.copyWith(
              titleSmall: const TextStyle(
            fontSize: 20,
            fontFamily: "Schyler",
          ),
        ),
      ),
      routes: {
        Rotas.HOME: (ctx) => TelaCategorias(),
        Rotas.PRODUTOS: (ctx) => FutureBuilder<List<dynamic>>(
          future: teste,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return Scaffold(
                body: Center(
                  child: CircularProgressIndicator(),
                ),
              );
            } else {
              if (snapshot.hasError) {
                return Scaffold(
                  body: Center(
                    child: Text('Erro ao carregar os produtos!'),
                  ),
                );
              } else {
                // Converte a lista dinâmica para List<Produto>
                List<Produto> produtos = (snapshot.data as List<dynamic>)
                    .map((item) => Produto.fromJson(item))
                    .toList();
                    print("Aqui aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa");
                print(produtos[0].title);
                return TelaProdutos(produtos);
              }
            }
          },
        ),
      },
    );
  }
}
