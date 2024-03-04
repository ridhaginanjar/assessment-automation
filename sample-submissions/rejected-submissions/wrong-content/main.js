const express = require('express');

const app = express();

app.get('/', (request, response) => {
  response.send('<h1>12345</h1>');
});

app.listen(5000, 'localhost');
