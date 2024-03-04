const http = require('http');

const server = http.createServer((request, response) => {
  response.writeHead(200, { 'Content-Type': 'text/html' });
  response.end('<h1>123456</h1>')
});

server.listen(5000, 'localhost')
