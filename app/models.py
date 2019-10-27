from . import db
from werkzeug.security import (generate_password_hash,
                               check_password_hash)
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, unique = True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    username = db.Column(db.String(255), primary_key = True, unique = True)
    email = db.Column(db.String(255), unique = True, index = True)
    bio = db.Column(db.String())
    avatar_path = db.Column(db.String(), primary_key = True, unique = True)
    password_hash = db.Column(db.String(255))
    posts = db.relationship("Post",
                            foreign_keys = "Post.user_id", 
                            backref = "user",
                            lazy = "dynamic")
    comments = db.relationship("Comment", 
                                foreign_keys = "Comment.user_id",
                                backref = "user",
                                lazy = "dynamic")
    post_name = db.relationship("Comment", 
                                foreign_keys = "Post.username",
                                backref = "user",
                                lazy = "dynamic")
    comment_name = db.relationship("Comment", 
                                foreign_keys = "Comment.username",
                                backref = "user",
                                lazy = "dynamic")
    post_avatar = db.relationship("Comment", 
                                foreign_keys = "Post.user_avatar",
                                backref = "user",
                                lazy = "dynamic")
    comment_avatar = db.relationship("Comment", 
                                foreign_keys = "Comment.user_avatar",
                                backref = "user",
                                lazy = "dynamic")
    liked = db.relationship("PostLike",
                            foreign_keys = "PostLike.user_id",
                            backref = "user", 
                            lazy = "dynamic")

    @property
    def password(self):
        raise AttributeError("You cannot read the password attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # User like logic
    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id = self.id, post_id = post.id)
            db.session.add(like)

    # User dislike logic
    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id = self.id,
                post_id = post.id).delete()

    # Check if user has liked post
    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0

    # string representaion to print out a row of a column, important in debugging
    def __repr__(self):
        return f"User {self.username}"

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True)
    post_title = db.Column(db.String)
    post_content = db.Column(db.Text)
    posted_at = db.Column(db.DateTime)
    upvotes = db.Column(db.Integer, default = 0)
    downvotes = db.Column(db.Integer, default = 0)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    posted_by = db.Column(db.String, db.ForeignKey("users.username"))
    user_avatar = db.Column(db.String, db.ForeignKey("users.avatar_path"))
    comments = db.relationship("Comment", 
                                foreign_keys = "Comment.post_id", 
                                backref = "post", 
                                lazy = "dynamic")

    def save_post(self):
        db.session.add(self)
        db.session.commit()

    def delete_post(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_user_posts(cls,id):
        posts = Post.query.filter_by(user_id = id).all()
        return posts

    @classmethod
    def get_all_posts(cls):
        return Post.query.order_by(Post.posted_at.asc()).all()

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.String)
    comment_at = db.Column(db.DateTime)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    posted_by = db.Column(db.String, db.ForeignKey("users.username"))
    user_avatar = db.Column(db.String, db.ForeignKey("users.avatar_path"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        comments = Post.query.filter_by(post_id = id).all()
        return comments

class PostLike(db.Model):
    __tablename__ = "post_like"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

class Quote:
    """
    Blueprint class for quotes consumed from API
    """
    def __init__(self, author, quote):
        self.author = author
        self.quote = quote