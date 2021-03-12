from app import db, User, Post, connect_db, app

def reset_db():
    """Drop all tables and create all tables"""
    connect_db(app)
    db.drop_all()
    db.create_all()

