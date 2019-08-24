from flask import render_template
from app import app
# package / flask instance

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