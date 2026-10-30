import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class Formulario extends StatefulWidget {
  @override
  _FormularioState createState() => _FormularioState();
}

class _FormularioState extends State<Formulario> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  TextEditingController _tituloController = TextEditingController();
  TextEditingController _imageUrlController = TextEditingController();
  TextEditingController _valorController = TextEditingController();
  TextEditingController _tempoPreparoController = TextEditingController();
  bool _freeGluten = false;
  bool _vegano = false;
  bool _vegetariano = false;
  bool _freeLactose = false;

  Future<void> enviarParaBancoDeDados() async {
    var url = Uri.parse('http://localhost:3000/adicionar_produto');
  var response = await http.post(
  url,
  body: {
    'titulo': _tituloController.text,
    'image_url': _imageUrlController.text,
    'valor': _valorController.text,
    'tempo_preparo': _tempoPreparoController.text,
    'free_gluten': _freeGluten.toString(),
    'vegano': _vegano.toString(),
    'vegetariano': _vegetariano.toString(),
    'free_lactose': _freeLactose.toString(),
  },
);
    if (response.statusCode == 200) {
      // Se a inserção for bem-sucedida, exiba uma mensagem
      print('Dados enviados para o banco de dados com sucesso!');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Dados enviados com sucesso!')),
      );
      // Limpar os campos do formulário após o envio bem-sucedido
      _tituloController.clear();
      _imageUrlController.clear();
      _valorController.clear();
      _tempoPreparoController.clear();
      setState(() {
        _freeGluten = false;
        _vegano = false;
        _vegetariano = false;
        _freeLactose = false;
      });
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
                controller: _imageUrlController,
                decoration: InputDecoration(
                  labelText: 'Imagem URL',
                  hintText: 'Digite a URL da imagem',
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Por favor, insira a URL da imagem';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _valorController,
                decoration: InputDecoration(
                  labelText: 'Valor',
                  hintText: 'Digite o valor',
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Por favor, insira o valor';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _tempoPreparoController,
                decoration: InputDecoration(
                  labelText: 'Tempo de Preparo',
                  hintText: 'Digite o tempo de preparo',
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Por favor, insira o tempo de preparo';
                  }
                  return null;
                },
              ),
              CheckboxListTile(
                title: Text('Sem Glúten'),
                value: _freeGluten,
                onChanged: (value) {
                  setState(() {
                    _freeGluten = value!;
                  });
                },
              ),
              CheckboxListTile(
                title: Text('Vegano'),
                value: _vegano,
                onChanged: (value) {
                  setState(() {
                    _vegano = value!;
                  });
                },
              ),
              CheckboxListTile(
                title: Text('Vegetariano'),
                value: _vegetariano,
                onChanged: (value) {
                  setState(() {
                    _vegetariano = value!;
                  });
                },
              ),
              CheckboxListTile(
                title: Text('Sem Lactose'),
                value: _freeLactose,
                onChanged: (value) {
                  setState(() {
                    _freeLactose = value!;
                  });
                },
              ),
              Padding(
                padding: EdgeInsets.symmetric(vertical: 16.0),
                child: ElevatedButton(
                  onPressed: () {
                    if (_formKey.currentState!.validate()) {
                            if (_tituloController.text.isNotEmpty &&
        _imageUrlController.text.isNotEmpty &&
        _valorController.text.isNotEmpty &&
        _tempoPreparoController.text.isNotEmpty) {
      // Se todos os campos estiverem preenchidos, envie os dados para o servidor
      enviarParaBancoDeDados();
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
