from flask import (render_template, request, redirect, 
                   url_for, abort)
from . import main
from ..models import User, Comment, Post
from flask_login import login_required, current_user
from datetime import datetime
from .. import db, photos

@main.route("/")
def index():
    posts = Post.get_all_posts()

    return render_template("index.html",
                            posts = posts)

@main.route("/post/<int:id>")
def post(id):
    post = Post.query.filter_by(id = id).first()

    return render_template("post.html",
                            post = post)

@main.route("/profile/<int:id>")
def profile():
    user = User.query.filter_by(id = id).first
    posts = Post.query.filter_by(user_id = id).all()
    return render_template("profile/profile.html",
                            user = user,
                            posts = posts)