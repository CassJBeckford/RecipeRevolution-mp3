from flask import Flask, render_template, request, redirect, url_for
from cookbook import app, db
from cookbook.models import Category, Recipe, Users


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
    recipes = list(Recipe.query.order_by(Recipe.id).all())
    return render_template("recipe.html", recipes=recipes)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    categories = list(Category.query.order_by(Category.category_title).all())
    if request.method == "POST":
        recipe = Recipe(
            recipe_name=request.form.get("recipe_name"),
            recipe_description=request.form.get("recipe_description"),
            recipe_instructions=request.form.get("recipe_instructions"),
            recipe_difficulty=request.form.get("recipe_difficulty"),
            recipe_time=request.form.get("recipe_time"),
            recipe_amount=request.form.get("recipe_amount"),
            category_id=request.form.get("category_id") 
        )
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for("recipe"))
        # add defensive programming 
    return render_template("add_recipe.html", categories=categories)


@app.route("/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    categories = list(Category.query.order_by(Category.category_title).all())
    if request.method == "POST":
        recipe.recipe_name=request.form.get("recipe_name"),
        recipe.recipe_description=request.form.get("recipe_description"),
        recipe.recipe_instructions=request.form.get("recipe_instructions"),
        recipe.recipe_difficulty=request.form.get("recipe_difficulty"),
        recipe.recipe_time=request.form.get("recipe_time"),
        recipe.recipe_amount=request.form.get("recipe_amount"),
        recipe.category_id=request.form.get("category_id")
        db.session.commit()
        return redirect(url_for("recipe"))
    return render_template("edit_recipe.html", recipe=recipe, categories=categories)

@app.route("/register")
def register():
    return render_template("register.html")