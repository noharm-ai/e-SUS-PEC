from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from ariadne.constants import PLAYGROUND_HTML
from ariadne import graphql_sync, make_executable_schema

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from .views import all_views
app.register_blueprint(all_views)

from .graphql import query, type_defs, resolvers
schema = make_executable_schema(type_defs, query)

# Create a GraphQL Playground UI for the GraphQL schema


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    # Playground accepts GET requests only.
    # If you wanted to support POST you'd have to
    # change the method to POST and set the content
    # type header to application/graphql
    return PLAYGROUND_HTML

# Create a GraphQL endpoint for executing GraphQL queries


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema, data, context_value={"request": request})
    status_code = 200 if success else 400
    return jsonify(result), status_code

# Create executable schema

# Later on you'll import the other blueprints the same way:
#from app.comments.views import mod as commentsModule
#from app.posts.views import mod as postsModule
# app.register_blueprint(commentsModule)
# app.register_blueprint(postsModule)
