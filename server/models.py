import re
from config import bcrypt, db
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, relationship
from datetime import datetime


# User #
class User(db.Model, SerializerMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    userName = Column(String(100), nullable=False, unique=True)
    _password_hash = Column(String(128), nullable=False)
    photo_user = db.Column(db.String(255))
    email = db.Column(db.String)
    phone = db.Column(db.Integer)
    about_me = db.Column(db.String(300))
    created_at = Column(DateTime, default=datetime.now)

    # Relationships
    recipes = relationship("Recipe", back_populates="user")
    comments = relationship("Comment", back_populates="user")

    # Serialization configuration
    serialize_rules = (
        "-recipes.user",
        "-comments",
        "-_password_hash",
        "-created_at",
        "-email",
        "-phone",
        "-about_me",
        "-photo_user",
    )

    @validates("userName")
    def validate_userName(self, _, userName):
        if not userName:
            raise ValueError("userName cannot be empty")
        if len(userName) > 10:
            raise ValueError("userName cannot exceed 10 characters")
        return userName

    @validates("about_me")
    def validate_about_me(self, _, about_me):
        if about_me and len(about_me) > 300:
            raise ValueError("about_me cannot exceed 300 characters")
        return about_me

    @validates("phone")
    def validate_phone(self, key, phone):
        if phone is None:
            return None  # Or handle this case based on your requirements

        phone = str(phone)  # Ensure phone is a string
        phone_digits = re.sub(r"\D", "", phone)

        if len(phone_digits) != 10:
            raise ValueError("Phone must be a 10-digit number.")

        return phone_digits

    @validates("email")
    def validate_email(self, _, email):
        if not isinstance(email, str):
            raise TypeError("Email must be a string.")
        elif not 5 <= len(email) <= 40:
            raise ValueError(f"Email must be between 5 and 40 characters.")
        email_regex = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format.")
        return email

    @hybrid_property
    def password_hash(self):
        raise AttributeError("password is not readable")

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    def __repr__(self):
        return f"User(id={self.id}, userName='{self.userName}', created_at='{self.created_at}', photo_url='{self.photo_user}', phone='{self.phone}', email='{self.email}', about_me='{self.about_me})"


# Recipe #
class Recipe(db.Model, SerializerMixin):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    ingredients = Column(Text, nullable=False)
    instructions = Column(Text, nullable=False)
    photo_url = db.Column(db.String(255))
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="recipes")
    comments = relationship("Comment", back_populates="recipe")
    tags = relationship("Tag", secondary="recipe_tags", back_populates="recipes")
    tag_names = association_proxy("tags", "category")

    # Serialization configuration
    serialize_rules = (
        "-user.recipes",
        "-comments.recipe",
        "-tags.recipes",
        "-created_at",
        "tags.category",
    )

    def __repr__(self):
        return f"Recipe(id={self.id}, title='{self.title}', description='{self.description}', ingredients='{self.ingredients}', instructions='{self.instructions}', photo_url='{self.photo_url}')"


# Food Type Tag #
class Tag(db.Model, SerializerMixin):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    category = Column(String(100), unique=True, nullable=False)

    # Relationships
    recipes = relationship("Recipe", secondary="recipe_tags", back_populates="tags")

    # Serialization configuration
    serialize_rules = ("-recipes.tags", "-created_at")

    serialize_only = ("id", "category")

    def __repr__(self):
        return f"Tag(id={self.id}, category='{self.category}')"


# Combines Tag With Recipe #
class RecipeTag(db.Model, SerializerMixin):
    __tablename__ = "recipe_tags"
    recipe_id = Column(
        Integer, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True
    )
    tag_id = Column(
        Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    )

    # Serialization configuration
    serialize_rules = ("-recipe", "-tag")

    def __repr__(self):
        return f"RecipeTag(recipe_id={self.recipe_id}, tag_id={self.tag_id})"


# Comment On Recipes #
class Comment(db.Model, SerializerMixin):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    comment = Column(String(300), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    recipe_id = Column(
        Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    recipe = relationship("Recipe", back_populates="comments")
    user = relationship("User", back_populates="comments")

    # Serialization configuration
    serialize_rules = (
        "-recipe",
        "-user.comments",
        "-user.recipes",
    )

    def __repr__(self):
        return f"Comment(id={self.id}, recipe_id={self.recipe_id}, user_id={self.user_id}, comment='{self.comment}')"
