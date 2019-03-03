from .server import app


print('Flask app running at 0.0.0.0:8886')
app.run(host='0.0.0.0', port=8886)