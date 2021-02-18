from flask import Flask

from app.blueprints import blueprints

from app.models import metadata

app = Flask(__name__)

app.url_map.strict_slashes = False

for blueprint in blueprints:
    app.register_blueprint(blueprint, url_prefix=f'/api/{blueprint.name}')
