// 1234567

/*
    1234567
 */

const express = require('express');
const dotenv = require('dotenv');

dotenv.config();
console.log(process.env.APP_HOST, process.env.APP_PORT)

const app = express();

app.get('/', (request, response) => {
  response.send('<h1>123456</h1>');
});

app.listen(Number(process.env.APP_PORT), process.env.APP_HOST);
