const express = require('express');

const app = express();

app.get('/', (request, response) => {
  response.send('<h1>123456</h1>');
});

app.listen(8080, 'localhost');
