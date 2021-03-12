"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Model for SQLAlchemy. Create users with a first name, last name, and image url"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False, default="https://static.toiimg.com/thumb/msid-67586673,width-600,height-600,resizemode-23,imgsize-3918697,pt-32,y_pad-40/67586673.jpg")
    posts = db.relationship("Post", backref="user", passive_deletes=True)

    def __repr__(self):
        return f"<User {self.id} {self.first_name} {self.last_name}>"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.String, nullable=False, default=datetime.now().strftime('%d, %b, %Y %X'))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'))
    
    def __repr__(self):
        return f"<Post {self.id} {self.title} {self.created_at} {self.user}>"