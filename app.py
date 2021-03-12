from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'heyeheye'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

#create - User
@app.route('/users/new')
def create_user_page():

    return render_template('new.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    """Create new user with information from forms"""
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    img_url = request.form["img-url"]
    new_user = User(first_name=first_name, last_name=last_name)
    if img_url:
        new_user.img_url = img_url

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

#create - Post
@app.route('/users/<user_id>/posts/new')
def create_post_page(user_id):
    user = User.query.get(user_id)

    return render_template('create-post.html', user=user)

@app.route('/users/<user_id>/posts/new', methods=['POST'])
def create_post(user_id):
    title = request.form['post-title']
    content = request.form['post-content']

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

#read - User
@app.route('/')
def homepage():
    
    return redirect('/users')

@app.route('/users')
def list_users():
    """List every user, using a query"""
    users = User.query.all()

    return render_template('list-users.html', users=users)

@app.route('/users/<user_id>')
def user_page(user_id):
    """Return page that corresponds to user_id"""
    user = User.query.get(user_id)
    return render_template('user.html', user=user)
    
#read - Post
@app.route('/posts/<post_id>')
def post_page(post_id):
    post = Post.query.get(post_id)
    print(post)
    return render_template('post.html', post=post)

#update - User
@app.route('/users/<user_id>/edit')
def edit_user_page(user_id):
    user = User.query.get(user_id)

    return render_template('edit-user.html', user=user)
    
@app.route('/users/<user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Edit user with information from form inputs, only if the input has data in it"""
    first_name = request.form["first-name"] 
    last_name = request.form["last-name"]
    img_url = request.form["img-url"]
    
    user = User.query.get(user_id)
    
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if img_url:
        user.img_url = img_url

    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{user_id}')

#update - Post
@app.route('/posts/<post_id>/edit')
def edit_post_Page(post_id):
    post = Post.query.get(post_id)

    return render_template('edit-post.html', post=post)

@app.route('/posts/<post_id>/edit', methods=['POST'])
def edit_post(post_id):
    
    title = request.form["post-title"] 
    content = request.form["post-content"]
    post = Post.query.get(post_id)
    
    if title:
        post.title = title
    if content:
        post.content = content

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

#delete - User
@app.route('/users/<user_id>/delete')
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()

    db.session.commit()

    return redirect('/')

#delete - Post
@app.route('/posts/<post_id>/delete')
def delete_post(post_id):
    Post.query.filter_by(id=post_id).delete()

    db.session.commit()

    return redirect('/')