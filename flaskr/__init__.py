import os
from flaskr.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
app.debug=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///headlines.sqlite3'

db = SQLAlchemy(app)


from flaskr import views
