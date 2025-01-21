from recipes import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_title = db.Column(db.String(25), unique=True, nullable=False)

    def __repr__(self):
        return self 


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return self 