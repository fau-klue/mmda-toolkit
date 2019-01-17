# __init__.py is a special Python file that allows a directory to become
# a Python package so it can be accessed using the 'import' statement.


from .admin_views import admin_blueprint
from .user_views import user_blueprint
from .login_views import login_blueprint
from .corpus_views import corpus_blueprint
from .coordinates_views import coordinates_blueprint
from .analysis_views import analysis_blueprint
from .discourseme_views import discourseme_blueprint
from .discursive_position_views import discursive_blueprint


def register_blueprints(app):
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(corpus_blueprint)
    app.register_blueprint(analysis_blueprint)
    app.register_blueprint(discourseme_blueprint)
    app.register_blueprint(coordinates_blueprint)
    app.register_blueprint(discursive_blueprint)
