from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'heyeheye'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

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
    

@app.route('/users/new')
def create_user_page():

    return render_template('new.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    """Create new user with information from forms"""
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    img_url = request.form["img-url"]

    newUser = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(newUser)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<user_id>/edit')
def edit_user_page(user_id):
    user = User.query.get(user_id)

    return render_template('edit-user.html', user=user)
    
@app.route('/users/<user_id>/edit', methods=["POST"])
"""Edit user with information from form inputs, only if the input has data in it"""
def edit_user(user_id):
    print(request.form)
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

@app.route('/users/<user_id>/delete')
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).delete()

    db.session.commit()

    return redirect('/')