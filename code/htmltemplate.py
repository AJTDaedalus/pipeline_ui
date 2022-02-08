from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/login")
def login():
    return render_template("index.html")
@app.route("/admin")
def admin():
    return render_template("index.html")
@app.route("/mypage1")
def mypage1():
    return render_template("index.html")
@app.route("/testnew")
def testnew():
    return render_template("new.html")



if __name__ == "__main__":
    app.run(debug=True)
