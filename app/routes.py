from flask import render_template, request, redirect, url_for, flash
from . import db
from .models import ToDo
from flask import current_app as app


@app.route("/")
def index():
    todos = ToDo.query.all()
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    description = request.form.get("description")
    if not title:
        flash("Title is required!", "error")
        return redirect(url_for("index"))
    new_todo = ToDo(title=title, description=description)
    db.session.add(new_todo)
    db.session.commit()
    flash("ToDo added successfully!", "success")
    return redirect(url_for("index"))


@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete(todo_id):
    todo = ToDo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash("ToDo deleted successfully!", "success")
    return redirect(url_for("index"))


@app.route("/toggle/<int:todo_id>", methods=["POST"])
def toggle(todo_id):
    todo = ToDo.query.get_or_404(todo_id)
    todo.done = not todo.done
    db.session.commit()
    flash("ToDo status updated!", "success")
    return redirect(url_for("index"))
