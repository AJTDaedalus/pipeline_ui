#code from https://hack4impact.github.io/flask-base/assets/
from app.models import Permission, User, Role
from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user
from app.home import home

def permission_required(permission):
    """Restrict a view to users with the given permission."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.query.filter(User.roles.any(Role.name==permission)).all():
                abort(403)
            return f(*args, **kwargs)
            #redirect(url_for("home.lacking_permission"))
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)
