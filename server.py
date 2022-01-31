from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/list")
def hello():
    return "Hello World!"

@app.route("/question/<question_id>")
def hello():
    return "Hello World!"

@app.route("/add-question")
def hello():
    return "Hello World!"

@app.route("/question/<question_id>/new-answer")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
