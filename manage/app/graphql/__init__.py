from ariadne import gql, QueryType, load_schema_from_path

# Define type definitions (schema) using file path route
# type_defs = load_schema_from_path("./app/graphql/schema.graphql")

# Define type definitions (schema) using SDL
type_defs = gql(
    """
   type Query {
       places: [Place]
       "Resolver para servir de fixture para models de outra aplicação Django. `model` é a string que deve aparecer no campo model, `table` no momento deve ser um dos: `[ciap, medicamento]`. Atenção, o campo `fields` está como **String**"
       fixtures(model:String!, table:String!): [Fixture!]
       prescriptions: [String]
   }


   type Place {
       name: String!
       description: String!
       country: String!
       }  

    type Fixture {
        pk: String
        model: String
        fields: String
    }
   """
)

# Initialize query
query = QueryType()
