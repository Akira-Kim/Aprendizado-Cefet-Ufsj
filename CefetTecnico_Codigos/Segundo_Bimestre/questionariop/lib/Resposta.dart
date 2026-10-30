import 'package:flutter/material.dart';

 class Resposta extends StatelessWidget {
  final String texto;
  final VoidCallback quandoSelecionar;

  Resposta(this.texto, this.quandoSelecionar);

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      margin: EdgeInsets.only(top: 10, bottom: 10),
      child: ElevatedButton(
        onPressed: quandoSelecionar,
        child: Text(texto),
      ),
    );
  }
}