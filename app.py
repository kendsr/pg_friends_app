from flask import Flask,render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)
## Change friend:app to appropriate user/password
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://friend:app@localhost:5432/friends_app'
db = SQLAlchemy(app)
title='PG Friends App'

# Create our database model
class Friend(db.Model):
    __tablename__ = "friends"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75))
    email = db.Column(db.String(120), unique=True)
    comments = db.Column(db.String(255))

    def __init__(self, name, email, comments):
        self.name = name
        self.email = email
        self.comments = comments

    def __repr__(self):
        return '<E-mail %r>' % self.email


# Landing Page
@app.route('/')
def home():
    return render_template('landing.html', title=title)

# show form to add new friend
@app.route('/friends/new')
def show_new_form():
    return render_template('new.html', title=title)

# Add a new friend
@app.route('/friends', methods=['POST'])
def add_friend():
    newfriend=Friend(request.form['name'], request.form['email'], request.form['comments'])
    db.session.add(newfriend)
    db.session.commit()
    return redirect('/friends')

# Index route - List all  Friends
@app.route('/friends')
def index():
    friends = Friend.query.all()
    return render_template('index.html', title=title, friends=friends)

# SHOW route - get info for one friend
@app.route('/friends/<int:id>')
def get_friend(id):
    friend = Friend.query.filter(Friend.id==id).first()
    return render_template('show.html', title=title, friend=friend)

# Edit route - Find and edit friends
@app.route('/friends/edit/<int:id>')
def edit_friend(id):
    friend = Friend.query.filter(Friend.id==id).first()
    return render_template('edit.html', title=title, friend=friend)

# Update route for Friend 
@app.route('/friends/update/<int:id>', methods=['POST'])
def update_friend(id):
    friend = Friend.query.filter_by(id=id).first()
    friend.name = request.form['name']
    friend.email = request.form['email']
    friend.comments = request.form['comments']
    db.session.commit()
    return redirect('/friends/' +  str(id))

# DELETE friend
@app.route('/friends/delete/<int:id>')
def delete_friend(id):
    me = Friend.query.filter_by(id=id).first()
    db.session.delete(me)
    db.session.commit()
    return redirect('/friends')

if __name__ == '__main__':
    app.run()