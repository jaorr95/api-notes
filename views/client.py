# Run with "python client.py"
from bottle import get, run, static_file

@get('/')
def index():
    return static_file('index.html', root=".")

@get("/static/css/<filepath:re:.*\\.css>")
def css(filepath):
    return static_file(filepath, root=".")

@get("/static/js/<filepath:re:.*\\.js>")
def css(filepath):
    return static_file(filepath, root=".")

run(host='0.0.0.0', port=5000)
