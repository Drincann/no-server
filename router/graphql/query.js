const {
  GraphQLObjectType,
  GraphQLFloat,
  GraphQLInt,
} = require('graphql');

const NOLevel = require('./type/NOLevel');

const analysisNOLevel = require('../../core/analysisNOLevel')

const joi = require('joi');

const paramsSchema = joi.object({
  minlat: joi.number().required(),
  maxlat: joi.number().required(),
  minlon: joi.number().required(),
  maxlon: joi.number().required(),
  year: joi.number().integer().min(2019).max(2019).default(2019),
  month: joi.number().integer().min(1).max(12),
});

module.exports = new GraphQLObjectType({
  name: 'query',
  fields: {
    NOLevel: {
      type: NOLevel,
      args: {
        minlat: { type: GraphQLFloat },
        maxlat: { type: GraphQLFloat },
        minlon: { type: GraphQLFloat },
        maxlon: { type: GraphQLFloat },
        year: { type: GraphQLInt },
        month: { type: GraphQLInt },
      },
      resolve: async (source, args) => {
        const { value: { minlat, maxlat, minlon, maxlon, year, month }, error } = paramsSchema.validate(args);
        if (error) {
          throw new Error(error.message);
        }
        const data = await analysisNOLevel({
          minlat, maxlat, minlon, maxlon
        }, year, month);

        if (data.code == 1) {
          throw new Error(data.message)
        }

        return data;
      }
    },
  }
});