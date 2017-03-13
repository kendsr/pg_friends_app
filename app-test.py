## Test application with hard coded data and no database

from flask import Flask,render_template, redirect, request

app = Flask(__name__)
title='PG Friends App'

# Test data
friends = [
    {'id': 1, 'name':'Spock', 'email': 's@startrek.com', 'comments':'First Officer'},
    {'id': 2, 'name':'Jim Kirk', 'email': 'jt@startrek.net', 'comments':'Retired Spaceship captain'},
    {'id': 3, 'name':'Spock', 'email': 's@startrek.net', 'comments':'Retired Science Officer'}
]
friend_count = 3

# Landing Page
@app.route('/')
def home():
    return render_template('landing.html', title=title)

# Index route - List all  Friends
@app.route('/friends')
def index():
    return render_template('index.html', title=title, friends=friends)

# show form to add new friend
@app.route('/friends/new')
def show_new_form():
    return render_template('new.html', title=title)

# Add a new friend
@app.route('/friends', methods=['POST'])
def add_friend():
    global friend_count
    friend_count += 1
    friend={'id':friend_count, 'name':request.form['name'], 'email':request.form['email'], 'comments':request.form['comments']}
    friends.append(friend)
    return redirect('/friends')

# SHOW route - get info for one friend
@app.route('/friends/<int:id>')
def get_friend(id):
    friend = [friend for friend in friends if friend['id'] == id]
    return render_template('show.html', title=title, friend=friend[0])

# DELETE friend
@app.route('/friends/delete/<int:id>')
def delete_friend(id):
    friend = [friend for friend in friends if friend['id'] == id]
    friends.remove(friend[0])
    return redirect('/friends')

# Edit route - Find and edit friends
@app.route('/friends/edit/<int:id>')
def edit_friend(id):
    friend = [friend for friend in friends if friend['id'] == id]
    return render_template('edit.html', title=title, friend=friend[0])

# Update route for Friend 
@app.route('/friends/update/<int:id>', methods=['POST'])
def update_friend(id):
    friend = [friend for friend in friends if friend['id'] == id] 
    friend[0]['name'] = request.form['name']
    friend[0]['email'] = request.form['email']
    friend[0]['comments'] = request.form['comments']
    return redirect('/friends')



if __name__ == '__main__':
    app.run(debug=True)