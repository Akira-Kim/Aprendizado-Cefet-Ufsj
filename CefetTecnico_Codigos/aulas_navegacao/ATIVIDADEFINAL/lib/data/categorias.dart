
import 'dart:convert' as convert;

import 'package:http/http.dart' as http;


Future<List<dynamic>> dados_categoria() async{
  final response = await http
      .get(Uri.parse('http://localhost:3000/categoria'));
  if (response.statusCode == 200) {
    var jsonResponse = convert.jsonDecode(response.body);
    return jsonResponse;
  } else {
    throw Exception('Falha ao ler categorias!');
  }
}
