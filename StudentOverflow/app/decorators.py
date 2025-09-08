from functools import wraps
from flask import redirect, url_for, flash, session

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user"):
            flash("Necesitas iniciar sesión.", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped