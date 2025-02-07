from flask import Flask, render_template, request, redirect, url_for, flash, session
from menu import app, db
from menu.models import Category, Recipe, Users


@app.route("/")
def home():
    categories = list(Category.query.order_by(Category.category_title).all())
    return render_template("home.html", categories=categories)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        already_user = Users.query.filter(Users.user_name == request.form.get("username").lower())

        if already_user:
            flash('username taken')
            return redirect(url_for("register"))

        user = Users(
            user_name=request.form.get("username").lower(),
            password=request.form.get("password")
        )

        db.session.add(user)
        db.session.commit()
        session["username"] = user.id
        flash('Welcome!')
        return redirect(url_for("home"))
    return render_template("register.html")


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        already_user = Users.query.filter(Users.user_name == request.form.get("username").lower())

        if already_user:
            session["username"] = user.id
            flash('Welcome back, {}!'.format(request.form.get("username")))
            return redirect(url_for("home"))
        else:
            flash('Sorry, this username or password doesnt exist')
            return redirect(url_for("sign_in"))

    return render_template("sign_in.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("sign_in"))


@app.route("/categories", methods=["GET", "POST"])
def categories():
    categories = list(Category.query.order_by(Category.category_title).all())
    return render_template("categories.html", categories=categories)

    # if "username" not in session:
    #    return redirect(url_for("sign_in"))
    # else:
    #    categories = list(Category.query.order_by(Category.category_title).all())
    #    return render_template("categories.html", categories=categories)

    # user = Users.query.filter_by(id=user_id)
    # request.method == "POST"
    # if user:
    #    user_categories = list(Category.query.filter_by(user_id=user_id).all())
    #    return render_template("categories.html", user_categories=user_categories, user_id=user_id)
    # return render_template("categories.html")


@app.route("/add_categories", methods=["GET", "POST"])
def add_categories():
   
    if request.method == "POST":
        category = Category(category_title=request.form.get("category_title"))
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories")) 

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

#    if "username" not in session:
#        return redirect(url_for("sign_in"))

    recipes = list(Recipe.query.order_by(Recipe.id).all())
    return render_template("recipe.html", recipes=recipes, )



@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():

    categories = list(Category.query.order_by(Category.category_title).all())
    if request.method == "POST":
        
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

@app.route("/your_recipes/<int:category_id>")
def your_recipes(category_id):

#    if "username" not in session:
#        return redirect(url_for("sign_in"))
    #categories = Category.query.get_or_404(Category.recipes)
    #categories=categories
    Category.category_title = request.form.get("category_title")
    category_id = Category.query.get_or_404(category_id)
    # recipes = db.session.query(Category, Recipe).order_by(Category.recipes).all()
    recipes = list(Category.query.order_by(Category.recipes).all())
    return render_template("your_recipes.html", recipes=recipes)


