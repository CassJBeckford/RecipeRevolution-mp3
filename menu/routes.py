from flask import Flask, render_template, request, redirect, url_for, flash, session
from menu import app, db
from menu.models import Category, Recipe, Users
from werkzeug.security import generate_password_hash, check_password_hash

# --- Home app route displays all categories --- #
@app.route("/")
def home():
    """
    Gets categories from database and displays them in the home.html page
    """
    categories = list(Category.query.order_by(Category.category_title).all())
    return render_template("home.html", categories=categories)

# --- your_recipe route displays all recipes in a specific category --- #
@app.route("/your_recipes/<int:category_id>/")
def your_recipes(category_id):
    """
    Gets all recipes and
    displays them in your_recipes.html
    """
    category = Category.query.get_or_404(category_id)
    return render_template("your_recipes.html", category=category)

# --- Register page ---#
@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Gets register.html template and form to Post,
    then adds the details to the User db
    """
    if request.method == "POST":
        # Check if username already exists in db
        already_user = Users.query.filter(
            Users.user_name == request.form.get("username").lower()).all()

        if already_user:
            flash('username taken')
            return redirect(url_for("register"))

        user = Users(
            user_name=request.form.get("username").lower(),
            password=generate_password_hash(request.form.get("password"))
        )

        db.session.add(user)
        db.session.commit()

        # put the new user into 'session' 
        session["username"] = request.form.get("username").lower()
        flash('Welcome!')
        return redirect(url_for("home"))
    return render_template("register.html")

# --- Sign In page --- #
@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    """
    Gets login.html template and form to Post,
    then checks if user is logged in the session
    then logs them into session.
    """
    if request.method == "POST":
        # check if username exists in db
        already_user = Users.query.filter(
            Users.user_name == request.form.get("username").lower()).all()

        if already_user:
            # ensure hashed password matches user input
            if check_password_hash(already_user[0].password, request.form.get("password")):
                flash('Welcome back, {}!'.format(request.form.get("username")))
                session["username"] = request.form.get("username").lower()
                return redirect(url_for("home"))
            else:
                # invalid password/username match
                flash('Sorry, this username or password doesnt exist')
                return redirect(url_for("sign_in"))

    return render_template("sign_in.html")


@app.route("/logout")
def logout():
    # remove user from session
    session.pop("username", None)
    return redirect(url_for("sign_in"))

# --- categories --- #
@app.route("/categories/", methods=["GET", "POST"])
def categories():
    """
    Gets the categories and displays them
    """
    # get categories list from database
    categories = list(Category.query.order_by(Category.category_title).all())
    return render_template("categories.html", categories=categories)

    # if "username" not in session:
    #    return redirect(url_for("sign_in"))
    # else:
    #   user = Users.query.get_or_404(user_id)
    #   return render_template("categories.html", user=user)

    # user = Users.query.filter_by(id=user_id)
    # request.method == "POST"
    # if user:
    #    user_categories = list(Category.query.filter_by(user_id=user_id).all())
    #    return render_template("categories.html", user_categories=user_categories, user_id=user_id)
    # return render_template("categories.html")

# --- Add categories --- #
@app.route("/add_categories", methods=["GET", "POST"])
def add_categories():
    """
    Gets the new category name from the form and adds it to categories database
    """
    if request.method == "POST":
        category = Category(category_title=request.form.get("category_title"))
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))

    return render_template("add_categories.html")

# --- edit categories --- #
@app.route("/edit_categories/<int:category_id>", methods=["GET", "POST"])
def edit_categories(category_id):
    """
    Gets the updated category name from the form and replaces the category name in the category database.
    """
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        category.category_title = request.form.get("category_title")
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("edit_categories.html", category=category)

# --- delete categories --- #
@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    """
    deletes selected category in the database.
    """
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("categories"))

# --- Recipes --- #
@app.route("/recipe")
def recipe():
    """
    Gets the recipes and displays them
    """

#    if "username" not in session:
#        return redirect(url_for("sign_in"))

    recipes = list(Recipe.query.order_by(Recipe.id).all())
    return render_template("recipe.html", recipes=recipes, )

# --- Add recipes --- #
@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    """
    Gets the new recipe info from the form and adds it to the recipes database
    """
    categories = list(Category.query.order_by(Category.category_title).all())
    if request.method == "POST":
        # update the POST method to reflect each of the fields that will be added from the form
        recipe = Recipe(
            id=request.form.get("id"),
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
    return render_template("add_recipe.html", categories=categories)

# --- edit recipes --- #
@app.route("/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    """
    Gets the existing recipe info and updates the recipes database
    """
    recipe = Recipe.query.get_or_404(recipe_id)
    categories = list(Category.query.order_by(Category.category_title).all())
    if request.method == "POST":
        recipe.recipe_name = request.form.get("recipe_name"),
        recipe.recipe_description = request.form.get("recipe_description"),
        recipe.recipe_instructions = request.form.get("recipe_instructions"),
        recipe.recipe_difficulty = request.form.get("recipe_difficulty"),
        recipe.recipe_time = request.form.get("recipe_time"),
        recipe.recipe_amount = request.form.get("recipe_amount"),
        recipe.category_id = request.form.get("category_id")
        db.session.commit()
        return redirect(url_for("recipe"))
    return render_template("edit_recipe.html", recipe=recipe, categories=categories)
