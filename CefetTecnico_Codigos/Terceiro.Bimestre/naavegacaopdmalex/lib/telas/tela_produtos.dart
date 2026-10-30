//import 'dart:ffi';

//import 'package:flutter/material.dart';

//import '../models/categorias.dart';

//class TelaProdutos extends StatefulWidget{
  //final List<Produto> produtosValidos;
  //TelaProdutos(this.produtosValidos);

  //@override
 //State<TelaProdutos> createState() => _TelaProdutosState();
//}

//class _TelaProdutosState extends State <TelaProdutos> {
  //String? tituloCategoria;
  //List<Produto>? displayProdutos;

//@override
  //void didChangeDependencies() {
    //final argumentosRota = ModalRoute.of(context)!.settings.arguments as Map<String, String>;
    //final tituloCategoria = argumentosRota ['title']!;
    //final categoryId = argumentosRota['id'];
    //displayProdutos = widget.produtosValidos.where((produto){
      //return produto.categories.contains(categoryId);
    //}).toList();
    //super.didChangeDependencies();
    //}
    //@override
    //Widget build(BuildContext context) {
      //return Scaffold(
//appBar: AppBar(title: Text(tituloCategoria!)),
//body: ListView.builder(
  
//), 
    //);
    //}
//}


import 'package:flutter/material.dart';
import 'package:naavegacaopdmalex/models/produtos.dart';

import '../componentes/produto_item.dart';

class TelaProdutos extends StatefulWidget {

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
    final argumentosRota =
        ModalRoute.of(context)!.settings.arguments as Map<String, String>;
    final tituloCategoria = argumentosRota['title']!;
    final categoryId = argumentosRota['id'];
    //montando vetor de produtos
    displayProdutos = widget.produtosValidos.where((produto) {
      return produto.categories.contains(categoryId!);
    }).cast<Produtos>().toList();
    super.didChangeDependencies();
  }
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
            duration: displayProdutos![index].duration.toDouble(),
            cost: displayProdutos![index].cost.toDouble(),
          );
          //return Text(displayProdutos[index].title);
        },
        itemCount: displayProdutos!.length,
      ),
    );
  }
}