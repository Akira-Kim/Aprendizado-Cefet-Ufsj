
class Produto {
  final String id;
  final List<String> categories;
  final String title;
  final String imageUrl;
  final String duration;
  final String cost;
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

  factory Produto.fromJson(Map<String, dynamic> data) {
    return Produto(
      id: data['id_produtos'].toString(),
      categories: [data['id_categoria'].toString()],
      title: data['titulo'],
      imageUrl: data['image_url'],
      duration: data['tempo_preparo'].toString(),
      cost: data['valor'].toString(),
      isGlutenFree: data['free_gluten'] == 1,
      isLactoseFree: data['free_lactose'] == 1,
      isVegan: data['vegano'] == 1,
      isVegetarian: data['vegetariano'] == 1,
    );
  }
}