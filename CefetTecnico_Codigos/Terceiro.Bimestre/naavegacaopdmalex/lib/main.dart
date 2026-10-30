import 'package:flutter/material.dart';

//depois de programar a tela
import 'Telas/tela_categoria.dart';
 
void main() => runApp(AppCardapio());
 // style: Theme.of(context).textTheme.titleSmall, vai no categoria
class AppCardapio extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Cardápio',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        fontFamily: 'Schyler',
        textTheme: ThemeData.light().textTheme.copyWith(
          titleSmall : const TextStyle(
            fontSize: 20,
            fontFamily: "Schyler"
          ) 
        )
      ),
      home: TelaCategorias(),
    );
  }
}
 
class PaginaInicial extends StatefulWidget {
  @override
  PaginaInicialState createState() => PaginaInicialState();
}
 
class PaginaInicialState extends State<PaginaInicial> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Cardápio'),
      ),
      body: Center(
        child: Text('Corpo do meu APP'),
      ),
    );
  }
}