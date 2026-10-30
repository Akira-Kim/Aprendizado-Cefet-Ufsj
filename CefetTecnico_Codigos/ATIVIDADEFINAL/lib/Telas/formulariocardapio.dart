import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class Formulariocard extends StatefulWidget {
  @override
  _FormulariocardState createState() => _FormulariocardState();
}

class _FormulariocardState extends State<Formulariocard> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  TextEditingController _tituloController = TextEditingController();
  TextEditingController _corController = TextEditingController();

  Future<void>  enviar() async {
   var url = Uri.parse('http://localhost:3000/adicionar_card');
   var body =  {
      'titulo': _tituloController.text,
      'cor': _corController.text,
    };
    print(body);
  var response = await http.post(
    url,
    body : body,
    headers: {
      "Context-Type": "application/x-www-form-urlencoded"
    }

  );

    if (response.statusCode == 200) {
      // Se a inserção for bem-sucedida, exiba uma mensagem
      print('Dados enviados para o banco de dados com sucesso!');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Dados enviados com sucesso!')),
      );
      // Limpar os campos do formulário após o envio bem-sucedido
      _tituloController.clear();
      _corController.clear();
    } else {
      // Caso contrário, exiba uma mensagem de erro
      print('Falha ao enviar os dados para o banco de dados.');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Falha ao enviar os dados!')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Formulário'),
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              TextFormField(
                controller: _tituloController,
                decoration: InputDecoration(
                  labelText: 'Título',
                  hintText: 'Digite o título',
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Por favor, insira o título';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _corController,
                decoration: InputDecoration(
                  labelText: 'Cor',
                  hintText: 'Digite a cor',
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Por favor, insira a cor';
                  }
                  return null;
                },
              ),
              Padding(
                padding: EdgeInsets.symmetric(vertical: 16.0),
                child: ElevatedButton(
                 onPressed: () {
                    if (_formKey.currentState!.validate()) {
                            if (_tituloController.text.isNotEmpty && _corController.text.isNotEmpty) {
      // Se todos os campos estiverem preenchidos, envie os dados para o servidor
      enviar();
    } else {
      // Se algum campo estiver vazio, exiba uma mensagem ao usuário
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Por favor, preencha todos os campos!')),
      );
    }
  }
},
                  child: Text('Enviar'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
