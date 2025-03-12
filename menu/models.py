from menu import db
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(260), nullable=False)

    def __repr__(self):
        return self.user_name


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_title = db.Column(db.String(25), unique=True, nullable=False)
    recipes = db.relationship("Recipe", backref="category", cascade="all, delete", lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return self.category_title


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(50), unique=True, nullable=False)
    recipe_description = db.Column(db.Text, nullable=False)
    recipe_instructions = db.Column(db.Text, nullable=False)
    recipe_difficulty = db.Column(db.Integer, nullable=False)
    recipe_time = db.Column(db.Text, nullable=False)
    recipe_amount = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return "#{0} - Recipe: {1} | Difficulty: {2}".format(
            self.id, self.recipe_name, self.recipe_amount
        )
