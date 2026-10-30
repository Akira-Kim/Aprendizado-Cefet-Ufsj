

import 'package:aulas_navegacao/data/categorias.dart';
import 'package:aulas_navegacao/models/categorias.dart';
import 'package:flutter/material.dart';
import '../componentes/categoria_item.dart';
import '../data/mock_data.dart';

class TelaCategorias extends StatefulWidget {
  

  @override
  State<TelaCategorias> createState() => _TelaCategoriasState();
}

class _TelaCategoriasState extends State<TelaCategorias> {
  late Future<List<dynamic>> categoriaFuturo;

 @override
  void initState() {
    super.initState();
    categoriaFuturo = dados_categoria();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar : AppBar(
        title: Text("Cardápio do CEFETMG"),
      ),
      body: Center(
        child: FutureBuilder<List<dynamic>>(
          future: categoriaFuturo,
          builder: (context, snapshot) {
            if(snapshot.hasData){
              return GridView.builder(
                gridDelegate:  const SliverGridDelegateWithMaxCrossAxisExtent( //basicamente uma barra de rolagem
                  maxCrossAxisExtent: 200, //cada elemento tem extensão de 200
                  childAspectRatio: 3/2, //proporção de cada elemento dentro do grid
                  crossAxisSpacing: 20, // eixo cruzado de 20
                  mainAxisSpacing: 20 //espaçamento no main olhar
                  ), 
                itemCount: snapshot.data!.length,
                itemBuilder: (context, index){
                  return CategoriaItem(
                    Categoria(
                          id: snapshot.data![index]['id_categoria'], 
                          titulo: snapshot.data![index]['titulo'],
                          color: Color(int.parse('0x${snapshot.data![index]['cor']}'))
                        ),  
                    );
                });
            } else if(snapshot.hasError){
              return Text('${snapshot.error}');
            }
            return const CircularProgressIndicator();
          }),
        ),
    );
  }
}