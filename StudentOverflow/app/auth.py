from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .supabase_client import supabase_auth, supabase_db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()
        try:
            res = supabase_auth.auth.sign_up({"email": email, "password": password})
            user = res.user
            
            supabase_db.table("profiles").upsert({"id": user.id, "email": email}).execute()
            flash("Revisa tu correo para confirmar la cuenta", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            flash(f"Error al registrar: {e}", "danger")
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()
        try:
            res = supabase_auth.auth.sign_in_with_password({"email": email, "password": password})
            session["access_token"] = res.session.access_token
            session["refresh_token"] = res.session.refresh_token
            session["user"] = {"id": res.user.id, "email": res.user.email}
            return redirect(url_for("q.index"))
        except Exception as e:
            flash(f"Credenciales inválidas: {e}", "danger")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("q.index"))