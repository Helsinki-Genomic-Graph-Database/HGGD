from os import getenv, environ
from flask import Flask

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes

if __name__ == "__main__":
    port = int(environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)