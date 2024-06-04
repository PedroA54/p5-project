from config import bcrypt, db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
import itertools

# Models


class User(db.Model, SerializerMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(100), nullable=False, unique=True)
    _password_hash = db.Column(db.String(128), nullable=False)

    # Relationships
    recipes = db.relationship("Recipe", backref="author", lazy=True)
    liked_recipes = db.relationship(
        "Recipe", secondary="likes", backref=db.backref("likes", lazy="dynamic")
    )

    # Serialization
    # Excludes recipes, liked recipes, and password ofc
    serialize_rules = ("-recipes.user", "-liked_recipes.liked_by", "-_password_hash")

    @validates("userName")
    def validate_userName(self, _, userName):
        if not userName:
            raise ValueError("userName cannot be empty")
        if len(userName) > 100:
            raise ValueError("userName cannot exceed 100 characters")
        return userName

    @hybrid_property
    def password_hash(self):
        raise AttributeError("password is not readable")

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    def __repr__(self):
        return f"User(id={self.id}, userName='{self.userName}')"


class Recipe(db.Model, SerializerMixin):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable=False)

    # Relationships
    tags = db.relationship(
        "Tag", secondary="recipe_tags", backref=db.backref("recipes", lazy="dynamic")
    )

    # Serialization
    # Exclude user and tag preventing circular rrefernce
    serialize_rules = ("-user.recipes", "-tags.recipes")

    def __repr__(self):
        return f"Recipe(id={self.id}, title='{self.title}', description='{self.description}', ingredients='{self.ingredients}', instructions='{self.instructions}')"


class Tag(db.Model, SerializerMixin):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), unique=True, nullable=False)

    # Serialization
    # Exclude recipes
    serialize_rules = ("-recipes.tags",)

    def __repr__(self):
        return f"Tag(id={self.id}, category='{self.category}')"


class RecipeTag(db.Model, SerializerMixin):
    __tablename__ = "recipe_tags"
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)


def __repr__(self):
    return f"RecipeTag(recipe_id={self.recipe_id}, tag_id={self.tag_id})"


class Like(db.Model, SerializerMixin):
    __tablename__ = "likes"
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)


def __repr__(self):
    return f"Like(recipe_id={self.recipe_id}, user_id={self.user_id})"
