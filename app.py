from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# mongodb://test:test@
client = MongoClient('localhost', 27017)
db = client.dbjungle

@app.route('/')


@app.route('/')
def home():
    return render_template('index.html')

client = MongoClient('localhost', 27017)
db = client.dbjungle

if __name__ == '__main__':
    app.run()
