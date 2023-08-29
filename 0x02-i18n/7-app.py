#!/usr/bin/env python3
"""A baisc flask app with i18n support
"""
from flask import Flask, render_template, g, request
from flask_babel import Babel
from pytz import timezone, UnknownTimeZoneError


class Config:
    """Representation of Locale config
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """Get user by ID
    """
    login_id = request.args.get('login_as')

    if login_id:
        return users.get(int(login_id))
    return None


@app.before_request
def before_request():
    """Run before any request
    """
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Retrieve user locale
    """
    # Locale from URL parameters
    locale = request.args.get('locale', '')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    # Locale from user settings
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']

    # Locale from request header
    header_locale = request.headers.get('locale', '')
    if header_locale in app.config['LANGUAGES']:
        return header_locale

    # Default locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


# babel.init_app(app, locale_selector=get_locale)


@babel.timezoneselector
def get_timezone():
    """Get user timezone
    """
    # timezone parameter from URL parameters
    tz = request.args.get('timezone', '').strip()
    if not tz and g.user:
        # timezone from the user settings
        tz = g.user['timezone']
    try:
        return timezone(tz).zone
    except UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


# @babel.init_app(app, timezone_selector=get_timezone)


@app.route('/')
def login():
    """Login user
    """
    return render_template('7-index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
