
import 'package:aulas_navegacao/models/categorias.dart';
import 'package:http/http.dart' as http;
import 'dart:convert' as convert;


Future<List<dynamic>> dados_categoria() async{
  final response = await http
      .get(Uri.parse('http://localhost:3001/categoria'));
  if (response.statusCode == 200) {
    var jsonResponse = convert.jsonDecode(response.body);
    return jsonResponse;
  } else {
    throw Exception('Falha ao ler categorias!');
  }
}