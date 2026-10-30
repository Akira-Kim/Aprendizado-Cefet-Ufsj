import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Mudança de Cores',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: ColorChangePage(),
    );
  }
}





class ColorChangePage extends StatefulWidget {
  @override
  _ColorChangePageState createState() => _ColorChangePageState();
}






class _ColorChangePageState extends State<ColorChangePage> {
  Color _backgroundColor = Color.fromARGB(255, 0, 0, 0);

  void _changeColor(Color color) {
    setState(() {
      _backgroundColor = color;
    });
  }





  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Mudança de Cores'),
      ),







      body: Container(
        color: _backgroundColor,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Mudança de Cores',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white),
            ),






            SizedBox(height: 20),
            Column(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [




                SizedBox(height: 20),
                SizedBox(width: 100),
                ElevatedButton(
                  onPressed: () => _changeColor(Colors.red),
                  child: Text('Vermelho'),
                  style: ElevatedButton.styleFrom(primary: Colors.red),
                ),




                SizedBox(height: 20),
                SizedBox(width: 100),
                ElevatedButton(
                  onPressed: () => _changeColor(Colors.green),
                  child: Text('Verde'),
                  style: ElevatedButton.styleFrom(primary: Colors.green),
                ),




                SizedBox(height: 20),
                SizedBox(width: 100),
                ElevatedButton(
                  onPressed: () => _changeColor(Colors.blue),
                  child: Text('Azul'),
                  style: ElevatedButton.styleFrom(primary: Colors.blue),
                ),


              ],
            ),
          ],
        ),
      ),
    );
  }
}
