import 'package:flutter/material.dart';

class Produtos {
  final String id;
  final String categories;
  final String title;
  final int cost;
  final String imageUrl;
  final int duration;
  final bool isGlutenFree;
  final bool isVegan;
  final bool isVegetarian;
  final bool isLactoseFree;

  const Produtos({
    required this.id,
    required this.categories,
    required this.title,
    required this.cost,
    required this.imageUrl,
    required this.duration,
    required this.isGlutenFree,
    required this.isVegan,
    required this.isVegetarian,
    required this.isLactoseFree,
  });
}
