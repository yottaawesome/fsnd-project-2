from flask import Flask, render_template, url_for, request, redirect, flash, jsonify

# Flask
app = Flask(__name__)

@app.route("/")
def restaurants():
    return render_template("index.html")

if __name__ == "__main__":
    app.debug = True
    app.run(host = "127.0.0.1", port = 5000)
