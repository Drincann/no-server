const koa = require('koa');
const koaRouter = require('koa-router');
const koaStatic = require('koa-static');
const router = require('./router');

const app = new koa();

app
  .use(koaStatic('./public', { defer: true }))
  .use(router.routes())
  .use(new koaRouter().allowedMethods());

app.listen(80);