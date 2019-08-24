from app import app
# package / flask instance
@app.route('/')
@app.route('/index')
# decorators : associate URL and arg given
def index():
    return "Hello, World!"