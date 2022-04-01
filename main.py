import flask
from flask import Flask, render_template, send_from_directory, send_file
from flask.views import MethodView

app = Flask(__name__)

class MainView(MethodView):
    def get(self):
        return flask.render_template("index.html")

if __name__ == "__main__":
    app.run(
        port=7777
    )


