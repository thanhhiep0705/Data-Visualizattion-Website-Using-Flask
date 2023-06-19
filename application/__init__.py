from flask import Flask, render_template


app = Flask(__name__)

app.config['TIMEOUT'] = 100

from application import routes