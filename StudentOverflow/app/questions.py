from flask import Blueprint, render_template, request, redirect, url_for, flash
from .supabase_client import supabase
from .decorators import login_required
from flask import session
import uuid

q_bp = Blueprint("q", __name__)

@q_bp.route("/")
def index():
    qs = supabase.table("questions").select("id, title, body, created_at, profiles(email)").order("created_at", desc=True).execute().data
    return render_template("index.html", questions=qs)

@q_bp.route("/ask", methods=["GET", "POST"])
@login_required
def ask():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        user = session.get("user")
        if not title:
            flash("El título es obligatorio.", "danger")
            return render_template("ask.html", title=title, body=body)
        supabase.table("questions").insert({
            "id": str(uuid.uuid4()),
            "user_id": user["id"],
            "title": title,
            "body": body
        }).execute()
        flash("Pregunta publicada.", "success")
        return redirect(url_for("q.index"))
    return render_template("ask.html")

@q_bp.route("/q/<id>")
def detail(id):
    q = supabase.table("questions").select("id, title, body, created_at, user_id, profiles(email)").eq("id", id).single().execute().data
    ans = supabase.table("answers").select("id, body, created_at, profiles(email)").eq("question_id", id).order("created_at").execute().data
    return render_template("detail.html", q=q, answers=ans)

@q_bp.route("/answer/<q_id>", methods=["POST"])
@login_required
def answer(q_id):
    body = request.form.get("body", "").strip()
    if not body:
        flash("La respuesta no puede estar vacía.", "danger")
        return redirect(url_for("q.detail", id=q_id))
    user = session.get("user")
    supabase.table("answers").insert({
        "question_id": q_id,
        "user_id": user["id"],
        "body": body
    }).execute()
    flash("Respuesta publicada.", "success")
    return redirect(url_for("q.detail", id=q_id))