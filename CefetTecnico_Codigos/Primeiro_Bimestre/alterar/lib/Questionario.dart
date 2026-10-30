import 'package:alterar/questao.dart';
import 'package:flutter/material.dart';
import 'package:alterar/Questao.dart';
import 'package:alterar/Resposta.dart';


 class Questionario extends StatelessWidget {
  
final List<Map<String, Object>> perguntas;
final int perguntaAtual;
final void Function() responder;


  Questionario({
    required this.perguntas,
    required this.perguntaAtual,
    required this.responder
  });

bool get tempergunta{


    return perguntaAtual < perguntas.length;

   }

   Widget build(BuildContext context){

    List<Widget> respostas = [];
   
if (tempergunta){

 for (var resposta in perguntas[perguntaAtual].cast()["respostas"]) {
      print(resposta);


      respostas.add(
          Resposta(resposta, responder)
        );
        
    }

}

return Column(children: <Widget>[
tempergunta

          ? Questao(perguntas[perguntaAtual]["texto"].toString())
          : Questao("Terminou"),

          tempergunta ? Column(
          children: [
            ...respostas,
          ],
        ): Text("Resultado")

],);
   }

 }









  

  @override
  Widget build(BuildContext context) {
    return Container(






    );
  }