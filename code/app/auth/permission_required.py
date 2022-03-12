#code from https://hack4impact.github.io/flask-base/assets/
from app.models import Permission
from functools import wraps
from flask import abort
from flask_login import current_user

def permission_required(permission):
    """Restrict a view to users with the given permission."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                redirect(url_for(home.lacking_permission))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)