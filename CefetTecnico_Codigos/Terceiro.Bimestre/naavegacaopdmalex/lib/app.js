const express = require('express')
const app = express()
const port = 3001
const mysql = require('mysql2');
var cors = require('cors')

const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password : "root",
    database: 'cardapio'
  });

app.use(cors())

app.get('/', (req, res) => {
  res.send('Alô mundo novo!')
})

app.get('/categoria', (req, res) => {
    connection.query(
        'SELECT * FROM categoria',
        function(err, results, fields) {
          res.send(results)
        }
      );
    
  })

app.get('/categoria/:id', (req, res) => {
    var id_categoria = req.params.id
    connection.query(
        'SELECT * FROM categoria where id_categoria = ' + id_categoria,
        function(err, results, fields) {
          res.send(results)
        }
      );
    
  })
app.post('/categoria', (req, res) => {
    console.log(req.body)
    var titulo = req.body
    connection.query(
        `insert into categoria(titulo) values("Chinesa")`,
        function(err, results, fields) {
            console.log(err)
          res.send(err)
        }
      );
    
  })
app.patch('/categoria/:id', (req, res) => {
    var id = req.params.id
    var titulo = "Chinesa nova"
    connection.query(
        `update categoria set titulo = "${titulo}" where id_categoria = ${id}`,
        function(err, results, fields) {
            console.log(err)
          res.send(err)
        }
      );
    
  })

app.get('/produto', (req, res) => {
    res.send('Acesso a rota produto!')
  })
  
app.post('/produto', (req, res) => {
    res.send('Acesso rota post!')
  })



app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})