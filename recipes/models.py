from recipes import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)