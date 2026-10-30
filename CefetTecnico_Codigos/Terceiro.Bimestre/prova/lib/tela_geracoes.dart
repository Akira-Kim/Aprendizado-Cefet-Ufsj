// tela_geracoes.dart

import 'package:flutter/material.dart';

import 'package:prova/generation_model.dart'; // Importe o modelo de dados
import 'package:prova/geracao.dart'; // Importe o widget GenerationItem

class GenerationsScreen extends StatelessWidget {
  final List<Generation> generations;

  GenerationsScreen({
    required this.generations,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Gerações de Pokémon"),
      ),
      body: ListView.builder(
        itemCount: generations.length,
        itemBuilder: (context, index) {
          final generation = generations[index];
          return GenerationItem(
            generation: generation,
            onTap: () {
              // Navegue para a tela de detalhes da geração
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => GenerationDetailsScreen(generation: generation),
                ),
              );
            },
          );
        },
      ),
    );
  }
}

class GenerationDetailsScreen extends StatelessWidget {
  final Generation generation;

  GenerationDetailsScreen({
    required this.generation,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(generation.title),
      ),
      body: ListView(
        children: [
          for (var images in generation.pokemons)
            Image.asset(images),
          // Outros detalhes da geração podem ser adicionados aqui
        ],
      ),
    );
  }
}
