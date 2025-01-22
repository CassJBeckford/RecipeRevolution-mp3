from flask import Flask, render_template
from recipes import app, db
from recipes.models import Category, Recipe


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/categories")
def categories():
    return render_template("categories.html")


@app.route("/add_categories", methods=["GET", "POST"])
def add_categories():
    return render_template("add_categories.html")


@app.route("/recipe")
def recipe():
    return render_template("recipe.html")