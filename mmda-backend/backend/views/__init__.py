"""
Import the blueprints here
"""


from .admin_views import admin_blueprint
from .user_views import user_blueprint
from .login_views import login_blueprint
from .corpus_views import corpus_blueprint
from .coordinates_views import coordinates_blueprint
from .analysis_views import analysis_blueprint
from .keyword_views import keyword_blueprint
from .discourseme_views import discourseme_blueprint
from .constellation_views import constellation_blueprint


def register_blueprints(app):
    """
    Register the blueprints here
    """

    app.register_blueprint(admin_blueprint)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(corpus_blueprint)
    app.register_blueprint(analysis_blueprint)
    app.register_blueprint(keyword_blueprint)
    app.register_blueprint(discourseme_blueprint)
    app.register_blueprint(coordinates_blueprint)
    app.register_blueprint(constellation_blueprint)
