from datetime import datetime
from flask import Flask
from app import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    header = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment_text = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    post_id = db.Column(
        db.Integer, 
        db.ForeignKey("post.id"),
        nullable=False,
        index=True
    )

    post = db.relationship(Post, foreign_keys=[post_id, ]) 
    



