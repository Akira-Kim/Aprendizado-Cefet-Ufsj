import 'package:flutter/material.dart';
import 'package:navegacao/componentes/produto_item.dart';
import 'package:navegacao/models/categorias.dart';
import '../models/produtos.dart';

class TelaProdutos extends StatefulWidget {
  static const routeName = '/produtos';
  final List<Produtos> produtosValidos;
  TelaProdutos(this.produtosValidos);

  @override
  State<TelaProdutos> createState() => _TelaProdutosState();
}

class _TelaProdutosState extends State<TelaProdutos> {
  String? tituloCategoria;
  List<Produtos>? displayProdutos;

  @override
  void didChangeDependencies() {
    // TODO: implement didChangeDependencies
    final routeArgs =
        ModalRoute.of(context)!.settings.arguments as Map<String, String>;
    tituloCategoria = routeArgs['title']!;
    final categoryId = routeArgs['id'];
    displayProdutos = widget.produtosValidos.where((meal) {
      return meal.categories.contains(categoryId);
    }).toList();
    super.didChangeDependencies();
  }

  // void _removeMeal(String mealId) {
  //   setState(() {
  //     displayedMeals!.removeWhere((meal) => meal.id == mealId);
  //   });
  // }

  // final String categoryId;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(tituloCategoria!)),
      body: ListView.builder(
        itemBuilder: (ctx, index) {
          return ItemProduto(
            id: displayProdutos![index].id,
            title: displayProdutos![index].title,
            imageUrl: displayProdutos![index].imageUrl,
            duration: displayProdutos![index].duration,
            cost: displayProdutos![index].cost,
          );
          // return Text(displayedMeals[index].title);
        },
        itemCount: displayProdutos!.length,
      ),
    );
  }
}

class TelaProdutos extends StatelessWidget {
  const TelaProdutos({super.key});


  @override
  Widget build(BuildContext context) {
  final categoria = ModalRoute.of(context)?.settings.arguments as Categoria;    
    
    return Scaffold(appBar: AppBar(
    title: Text("Tela Produtos"),
    
    ),
    body: Text("A categoria escolhida foi ${categoria.titulo}"),

    
    
    
    );
  }
}