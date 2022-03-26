#code modified from https://hack4impact.github.io/flask-base/assets/
from app.models import User, Role
from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user
from app.home import home

''' The following decorator can be applied to any view
    (see home/views or auth.views for views).
    The variable 'permission' is whichever role you want
    the user to need in order to access the view.
 '''
def permission_required(role):
    """Restrict a view to users with the given permission."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            authorized = User.query.filter(User.roles.any(name=role)).all()
            if current_user not in authorized:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
