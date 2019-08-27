from flask import render_template, flash, redirect, url_for
from app import app
# package / flask instance
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
# decorators : associate URL and arg given
def index():
    user = {'username': 'Mohamed'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    # list of dictio with author and body fields
    return render_template('index.html', title='Home', user=user, posts=posts)
# fct convert temp to HTML

@app.route('/login', methods=['GET', 'POST'])
# accept GET and POST requests
def login():
    form = LoginForm()
    if form.validate_on_submit():
    # do all the form precessing work
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    # if false render back form to user 
    return render_template('login.html', title='Sign In', form=form)