const {
  GraphQLObjectType,
  GraphQLString,
  GraphQLInt
} = require('graphql');

const NOLevel = new GraphQLObjectType({
  name: 'NOLevel',
  fields: {
    imgBase64: {
      type: GraphQLString,
      resolve: (source) => source.imgBase64,
    },
    code: {
      type: GraphQLInt,
      resolve: (source) => source.code,
    },
    message: {
      type: GraphQLString,
      resolve: (source) => source.message,
    },
  }
});

module.exports = NOLevel;