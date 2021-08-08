""" App principal file. """

#Flask
#from flask import Flask, request, render_template
from flask_cors import CORS

# package app
from app import create_app


app = create_app()
CORS(app, resources={r"api/v1/*": {"origins": "*"}})

@app.route('/', methods=['GET', 'POST'])
def hello():
    return "Hello"

if __name__ == '__main__':
    app.run(debug=True)