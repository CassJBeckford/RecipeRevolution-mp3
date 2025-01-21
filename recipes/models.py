from recipes import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_title = db.Column(db.String(25), unique=True, nullable=False)

    def __repr__(self):
        return self.category_title


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(50), unique=True, nullable=False)
    recipe_description = db.Column(db.Text, nullable=False)
    recipe_difficulty = db.Column(db.Integer(10), nullable=False)
    recipe_time = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self 