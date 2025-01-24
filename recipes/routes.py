from flask import Flask, render_template, request, redirect, url_for
from recipes import app, db
from recipes.models import Category, Recipe


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/categories")
def categories():
    categories = list(Category.query.order_by(Category.category_title).all())
    return render_template("categories.html", categories=categories)


@app.route("/add_categories", methods=["GET", "POST"])
def add_categories():
    if request.method == "POST":
        category = Category(category_title=request.form.get("category_title"))
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))
        # add defensive programming 
    return render_template("add_categories.html")


@app.route("/edit_categories/<int:category_id>", methods=["GET", "POST"])
def edit_categories(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        category.category_title = request.form.get("category_title")
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("edit_categories.html", category=category)
    

@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("categories"))


@app.route("/recipe")
def recipe():
    return render_template("recipe.html")