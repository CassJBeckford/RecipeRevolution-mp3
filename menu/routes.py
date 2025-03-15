from flask import render_template, request, redirect, url_for, flash
from menu import app, db
from menu.models import Category, Recipe, Users
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

# --- login_manager --- #
"""
Add login_manager to allow my application and Flask_Login to work together
"""
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "sign_in"


@login_manager.user_loader
def load_user(user_id):
    """
    Provide a user_loader callback to reload the user object from the user ID
    """
    return Users.query.get(int(user_id))

# --- Register and Login forms --- #


class RegisterForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    user_name = StringField("username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    user_name = StringField("username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


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
    form = RegisterForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(user_name=form.user_name.data).first()
        if user is None:
            password_hashed = generate_password_hash(form.password.data)
            user = Users(user_name=form.user_name.data,
                         password=password_hashed)
            db.session.add(user)
            db.session.commit()
            form.name.data = ""
            form.user_name.data = ""
            form.password.data = ""
            flash("Welcome!")
            return redirect(url_for("home"))
        else:
            flash("username taken")
            return redirect(url_for("register"))

    return render_template("register.html", form=form)


# --- Sign In page --- #
@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    """
    Gets login.html template and form to Post,
    then checks if user is logged in the session
    then logs them into session.
    """
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(user_name=form.user_name.data).first()
        if user:
            # Check the hash
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Welcome back!")
                return redirect(url_for("categories"))
            else:
                flash("Wrong Password")
        else:
            flash("That User Doesn't Exist")

    return render_template("sign_in.html", form=form)


@app.route("/logout")
@login_required
def logout():
    # remove user from session
    logout_user()
    return redirect(url_for("sign_in"))


# --- categories --- #
@app.route("/categories", methods=["GET", "POST"])
@login_required
def categories():
    """
    Gets the categories and displays them
    """
    # get categories list from database

    categories = list(Category.query.filter_by(user_id=current_user.id).all())
    return render_template("categories.html", categories=categories)


# --- Add categories --- #
@app.route("/add_categories", methods=["GET", "POST"])
@login_required
def add_categories():
    """
    Gets the new category name from the form and adds it to categories database
    """
    if request.method == "POST":
        category = Category(
            category_title=request.form.get("category_title"),
            user_id=current_user.id
        )
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))

    return render_template("add_categories.html")


# --- edit categories --- #
@app.route("/edit_categories/<int:category_id>", methods=["GET", "POST"])
def edit_categories(category_id):
    """
    Gets the updated category name from the form and replaces the category
    name in the category database.
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
@login_required
def recipe():
    """
    Gets the recipes and displays them
    """
    recipes = list(Recipe.query.filter_by(user_id=current_user.id).all())
    return render_template(
        "recipe.html",
        recipes=recipes,
    )


# --- Add recipes --- #
@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    """
    Gets the new recipe info from the form and adds it to the recipes database
    """
    categories = list(Category.query.order_by(Category.category_title).all())
    if request.method == "POST":
        # update the POST method to reflect each of the form fields.
        recipe = Recipe(
            id=request.form.get("id"),
            recipe_name=request.form.get("recipe_name"),
            recipe_description=request.form.get("recipe_description"),
            recipe_instructions=request.form.get("recipe_instructions"),
            recipe_difficulty=request.form.get("recipe_difficulty"),
            recipe_time=request.form.get("recipe_time"),
            recipe_amount=request.form.get("recipe_amount"),
            category_id=request.form.get("category_id"),
            user_id=current_user.id,
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
        recipe.recipe_name = (request.form.get("recipe_name"),)
        recipe.recipe_description = (request.form.get("recipe_description"),)
        recipe.recipe_instructions = (request.form.get("recipe_instructions"),)
        recipe.recipe_difficulty = (request.form.get("recipe_difficulty"),)
        recipe.recipe_time = (request.form.get("recipe_time"),)
        recipe.recipe_amount = (request.form.get("recipe_amount"),)
        recipe.category_id = request.form.get("category_id")
        db.session.commit()
        return redirect(url_for("recipe"))
    return render_template("edit_recipe.html", recipe=recipe,
                           categories=categories)


@app.route("/delete_recipe/<int:recipe_id>")
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for("recipe"))
