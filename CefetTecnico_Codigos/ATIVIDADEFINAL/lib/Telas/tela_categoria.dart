import 'package:aulas_navegacao/Telas/formulariocardapio.dart';
import 'package:aulas_navegacao/data/categorias.dart';
import 'package:aulas_navegacao/models/categorias.dart';
import 'package:flutter/material.dart';

import '../componentes/categoria_item.dart';
import 'formulario.dart'; // Importe a tela do formulário

class TelaCategorias extends StatefulWidget {
  @override
  State<TelaCategorias> createState() => _TelaCategoriasState();
}

class _TelaCategoriasState extends State<TelaCategorias> {
  late Future<List<dynamic>> categoriaFuturo;

  @override
  void initState() {
    super.initState();
    categoriaFuturo = dados_categoria() as Future<List>;
  }

  Color hexToColor(String code) {
    return Color(int.parse('0x$code'));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Cardápio do CEFETMG"),
      ),
      body: Center(
        child: FutureBuilder<List<dynamic>>(
          future: categoriaFuturo,
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              return GridView.builder(
                gridDelegate:
                    const SliverGridDelegateWithMaxCrossAxisExtent(
                  maxCrossAxisExtent: 200,
                  childAspectRatio: 3 / 2,
                  crossAxisSpacing: 20,
                  mainAxisSpacing: 20,
                ),
                itemCount: snapshot.data!.length,
                itemBuilder: (context, index) {
                  return CategoriaItem(
                    Categoria(
                      id: snapshot.data![index]['id_categoria'],
                      titulo: snapshot.data![index]['titulo'],
                      color: hexToColor(snapshot.data![index]['cor'].toString()),
                    ),
                  );
                },
              );
            } else if (snapshot.hasError) {
              return Text('${snapshot.error}');
            }
            return const CircularProgressIndicator();
          },
        ),
      ),
      floatingActionButton: Row( // Usando Row para posicionar os botões horizontalmente
        mainAxisAlignment: MainAxisAlignment.end, // Alinhamento para a extremidade direita
        children: [
          FloatingActionButton(
            onPressed: () {
              // Navega para a tela do formulário ao pressionar o botão
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => Formulario(),
                ),
              );
            },
            child: Icon(Icons.add),
          ),
          SizedBox(width: 16), // Adiciona um espaço entre os botões
          FloatingActionButton(
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                 builder: (context) => Formulariocard(),
                ),
              );
            },
            child: Icon(Icons.add),
          ),
        ],
      ),
    );
  }
}