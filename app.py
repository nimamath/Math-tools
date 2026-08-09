from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/quadratic")
def quadratic():
    return render_template("quadratic.html")


@app.route("/graph")
def graph():
    return render_template("graph.html")


@app.route("/system")
def system():
    return render_template("system.html")


if __name__ == "__main__":
    app.run()
