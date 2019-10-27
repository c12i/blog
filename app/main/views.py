from flask import (render_template, request, redirect, 
                   url_for, abort)
from . import main
from ..models import User, Comment, Post
from flask_login import login_required, current_user
from .forms import (UpdateProfile, PostForm, 
                    CommentForm, UpdatePostForm)
from datetime import datetime
import bleach
from .. import db, photos
from ..requests import get_quote

@main.route("/")
def index():
    posts = Post.get_all_posts()
    quote = get_quote()
    return render_template("index.html",
                            posts = posts,
                            quote = quote)

@main.route("/post/<int:id>", methods = ["POST", "GET"])
def post(id):
    post = Post.query.filter_by(id = id).first()
    comments = Comment.query.filter_by(post_id = id).all()
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        comment = comment_form.comment.data
        comment_form.comment.data = ""
        comment_alias = comment_form.alias.data
        comment_form.alias.data = ""
        if current_user.is_authenticated:
            comment_alias = current_user.username
        new_comment = Comment(comment = comment, 
                            comment_at = datetime.now(),
                            comment_by = comment_alias,
                            post_id = id,
                            user_id = current_user.id)
        new_comment.save_comment()
        return redirect(url_for("main.post", id = post.id))

    return render_template("post.html",
                            post = post,
                            comments = comments)

@main.route("/post/<int:id>/update", methods = ["POST", "GET"])
def edit_post(id):
    post = Post.query.filter_by(id = id).first()
    edit_form = UpdatePostForm()

    if edit_form.validate_on_submit():
        post_title = edit_form.title.data
        edit_form.title.data = ""
        post_content = edit_form.post.data
        edit_form.post.data = ""
        new_post = Post(post_title = post_title,
                        post_content = post_content,
                        posted_at = datetime.now(),
                        post_by = current_user.username,
                        user_id = current_user.id)
        new_post.save_post()
        return redirect(url_for("main.post", id = post.id))

    return render_template("edit_post.html", 
                            post = post,
                            edit_form = edit_form)

@main.route("/post/new", methods = ["POST", "GET"])
def new_post():
    post_form = PostForm()
    if post_form.validate_on_submit():
        post_title = post_form.title.data
        post_form.title.data = ""
        post_content = bleach.clean(post_form.post.data, 
                                    tags = bleach.sanitizer.ALLOWED_TAGS)
        post_form.post.data = ""
        new_post = Post(post_title = post_title,
                        post_content = post_content,
                        posted_at = datetime.now(),
                        post_by = current_user.username,
                        user_id = current_user.id)
        new_post.save_post()
        return redirect(url_for("main.index"))
    
    return render_template("new_post.html",
                            post_form = post_form)

@main.route("/profile/<int:id>")
def profile(id):
    user = User.query.filter_by(id = id).first
    posts = Post.query.filter_by(user_id = id).all()
    return render_template("profile/profile.html",
                            user = user,
                            posts = posts)