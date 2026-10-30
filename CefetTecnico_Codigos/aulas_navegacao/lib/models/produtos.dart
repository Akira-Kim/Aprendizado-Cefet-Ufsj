
class Produto {
  final String id;
  final List<String> categories;
  final String title;
  final String imageUrl;
  final double duration;
  final double cost;
  final bool isGlutenFree;
  final bool isLactoseFree;
  final bool isVegan;
  final bool isVegetarian;

  const Produto(
      {required this.id,
      required this.categories,
      required this.title,
      required this.imageUrl,
      required this.duration,
      required this.cost,
      required this.isGlutenFree,
      required this.isLactoseFree,
      required this.isVegan,
      required this.isVegetarian});
}