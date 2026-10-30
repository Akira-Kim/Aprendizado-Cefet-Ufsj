import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: ChatScreen(),
    );
  }
}

class ChatScreen extends StatefulWidget {
  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  TextEditingController _textEditingController = TextEditingController();
  List<String> componenteresposta = [];

  void _sendMessage() {
    setState(() {
      String message = _textEditingController.text;
      componenteresposta.add(message);
      _textEditingController.clear();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Componente Resposta'),
        backgroundColor: Colors.red,
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: componenteresposta.length,
              itemBuilder: (BuildContext context, int index) {
                return ListTile(
                  title: Text(componenteresposta[index]),
                );
              },
            ),
          ),
          Divider(),
          Container(
            padding: EdgeInsets.symmetric(horizontal: 10.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _textEditingController,
                    decoration: InputDecoration(
                      hintText: 'Digite sua resposta...',
                    ),
                  ),
                ),

                
                ElevatedButton(
                  onPressed: _sendMessage,
                  child: Text('Enviar'),
                  style: ElevatedButton.styleFrom(
    primary: Color.fromARGB(255, 255, 0, 0),
                  )
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}