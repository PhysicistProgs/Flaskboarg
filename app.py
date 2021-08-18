from flask import Flask, config, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy


import config

app = Flask(__name__, template_folder="templates")
app.config.from_object(config)

db = SQLAlchemy(app)

@app.route("/posts", methods=["GET"])
def view_articles():
    from models import Post, Comment
    posts = Post.query.all()
    comments = Comment.query.all()
    print(posts)
    return render_template("template.html", posts=posts, comments=comments)

@app.route("/write", methods=["GET", "POST"])
def write_article():
    from forms import PostForm
    from models import Post
    
    if request.method == "GET":
        return render_template("form.html")
    else:
        form = PostForm(request.form)
        posts = Post.query.all()
        if form.validate:
            post = Post(**form.data)
            db.session.add(post)
            db.session.commit()
            flash("Ok, posting it")
            posts = Post.query.all()
        else:
            flash("Not posted", str(form.errors))
        return render_template("template.html", posts=posts)

@app.route("/comment/<int:post_id>", methods=["GET", "POST"])
def write_comment(post_id):

    from forms import CommentForm
    from models import Comment, Post
    
    if request.method == "POST":
        form = CommentForm(request.form)
        posts = Post.query.all()
        comments = Post.query.all()
        if post_id < len(posts):
            
            if form.validate():
                print("*****FORM.DATA:", form.data)
                post = Post.query.filter_by(id=post_id).first()
                comment = Comment(post=post, **form.data)
                db.session.add(comment)
                db.session.commit()
                flash("Ok, posting it")
                comments = Comment.query.all()

            else:
                flash("Not posted", str(form.errors))
        else:
            flash("there is no post with this id")
    else:
        return render_template("form.html")

    return render_template("with_comments.html", comments=comments, posts=posts)

if __name__=="__main__":
    from models import *
    db.create_all()
    app.run()
