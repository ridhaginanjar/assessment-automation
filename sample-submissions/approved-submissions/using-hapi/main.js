// 1234567

/*
    1234567
 */

const Hapi = require('@hapi/hapi');

(async () => {
  const server = Hapi.server({
    host: 'localhost',
    port: 5000
  });

  server.route({
    path: '/',
    method: 'GET',
    handler: () => '<h1>123456</h1>',
  });

  await server.start();

  console.log(`server start at ${server.info.uri}`);
})()
