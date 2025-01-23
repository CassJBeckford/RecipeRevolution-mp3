from flask import Flask, render_template, request, redirect, url_for
from recipes import app, db
from recipes.models import Category, Recipe


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/categories")
def categories():
    categories = list(Category.query.order_by(Category.category_title).all())
    return render_template("categories.html")


@app.route("/add_categories", methods=["GET", "POST"])
def add_categories():
    if request.method == "POST":
        category = Category(category_title=request.form.get("category_title"))
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))
        # add defensive programming 
    return render_template("add_categories.html")


@app.route("/recipe")
def recipe():
    return render_template("recipe.html")