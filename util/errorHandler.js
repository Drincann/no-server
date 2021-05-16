module.exports = (error, ctx) => {
  ctx.body = { code: 1, message: error.message }
};