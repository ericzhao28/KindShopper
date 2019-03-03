from .server import app


print('Flask app running at localhost:8886')
app.run(host='localhost', port=8886, ssl_context='adhoc')