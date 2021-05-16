const joi = require('joi');
const koaRouter = require('koa-router');
const graphqlApi = require('./graphql');
const errorHandler = require('../util/errorHandler');

const router = new koaRouter();

const paramsSchema = joi.object({
  query: joi.string().required(),
  variables: joi.string(),
})

router.get('/graphql', async (ctx) => {
  try {
    const {
      value: params,
      error,
    } = paramsSchema.validate(ctx.query);

    if (error) {
      throw new Error(error.message);
    }

    ctx.body = await graphqlApi(params, ctx);
  } catch (error) {
    errorHandler(error, ctx)
  }
})

module.exports = router;