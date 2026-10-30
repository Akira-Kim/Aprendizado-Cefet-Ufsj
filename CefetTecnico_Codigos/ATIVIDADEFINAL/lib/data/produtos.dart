
import 'dart:convert' as convert;

import 'package:aulas_navegacao/models/produtos.dart';
import 'package:http/http.dart' as http;


Future<List<dynamic>> categoria_produtos() async{
  final response = await http
      .get(Uri.parse('http://localhost:3000/categoria_produto'));
  if (response.statusCode == 200) {
    var jsonResponse = convert.jsonDecode(response.body);
    print(jsonResponse);
    return jsonResponse;
  } else {
    throw Exception('Falha ao ler categorias!');
  }
}
