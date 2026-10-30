import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.red,
      ),
      home: Scaffold(
        appBar: AppBar(
          title: Text('Bruno Rabelo de Andrade Mateus'),
        ),
        body: Center(
          child: MyColumn(),
        ),
      ),
    );
  }
}

class MyColumn extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        ElevatedButton(
          onPressed: () {
          },
          child: Text('Enviar'),
        ),
        SizedBox(height: 16), 
        ElevatedButton(
          onPressed: () {
          },
          child: Text('Cancelar'),
        ),
        SizedBox(height: 16), 
        ElevatedButton(
          onPressed: () {
          },
          child: Text('Salvar'),
        ),
        SizedBox(height: 100),
        Column(
          children: [
            Text('Aprendendo'),
            Text('Programação'),
            Text('Flutter'),
          ],
        ),
      ],
    );
  }
}