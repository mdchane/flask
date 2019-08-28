from app import app, db
# top-lvl script import flask instance
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
# app.shell_ctxt_proc dctor registers the func as a shell context func