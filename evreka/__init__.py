from flask import Flask
from flask import Blueprint
from flask_graphql import GraphQLView

routes = Blueprint('routes', __name__)


@routes.route('/', methods=['GET', 'POST'])
def home():
    return "<p>Hello, World!</p>"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SECRET_KEY'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Oguz2011@127.0.0.1:33060/law-office-web'
    app.register_blueprint(routes, url_prefix='/')

    from evreka.schema import schema
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True  # Habilita la interfaz GraphiQL
        )
    )

    # with app.app_context():
    #     db.create_all()
    return app
