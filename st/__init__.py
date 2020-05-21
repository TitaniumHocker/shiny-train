# -*- coding: utf-8 -*-
from flask import Flask
from config import configurations as cfgs
from st.exceptions import InvalidConfigurationType
from st.extensions import migrate, security, user_datastore, babel, mail
from st.forms import CustomSendConfirmationForm
from st.blueprints import public
from st.models import db
from st.admin import admin


def create_app(mode='dev'):
    try:
        cfg = cfgs[mode]
    except KeyError:
        raise InvalidConfigurationType(
            'Unknown config type, try "prod", "dev" or "test".'
        )
    app = Flask(__name__)
    app.config.from_object(cfg)
    db.init_app(app)
    migrate.init_app(app, db)
    security.init_app(app, user_datastore,
                      send_confirmation_form=CustomSendConfirmationForm)
    mail.init_app(app)
    babel.init_app(app)
    admin.init_app(app)

    app.register_blueprint(public, url_prefix='/')
    # return app
    return app
