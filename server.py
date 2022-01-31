from flask import Flask, render_template, request, redirect, url_for

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

@app.route("/add-question", methods=['GET','POST'])
def hello():
    if request.method == 'GET':
        return render_template('add-question.html')
    elif request.method == 'POST':
        return render_template('index.html')
    return "Hello World!"

@app.route("/question/<question_id>/new-answer")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
