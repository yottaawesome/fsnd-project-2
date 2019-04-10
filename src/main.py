from flask import Flask, render_template, url_for, request, redirect, flash, jsonify

# Flask
app = Flask(__name__)

@app.route("/")
def restaurants():
    return render_template("index.html", restaurants=restaurants)
