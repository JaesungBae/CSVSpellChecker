import flask
from flask import Flask, render_template, send_from_directory, send_file
from flask import request
from flask.views import MethodView
from werkzeug.utils import secure_filename
import csv
import pandas as pd

from hanspell import spell_checker

app = Flask(__name__)

class MainView(MethodView):
    def get(self):
        return flask.render_template("index.html")

    def post(self):
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save("current_processing_file.csv".format(filename))

        col_names = ['input']
        csvData = pd.read_csv("current_processing_file.csv", names=col_names, header=None, encoding='cp949')
        if len(csvData) > 0:
            for i, row in csvData.iterrows():
                print(i, row['input'])
                app.add_url_rule(
                    "/processing{}/".format(i),
                    view_func=SpellCheckerView.as_view(
                        "processing{}".format(i),
                        max_idx=len(csvData),
                        cur_idx=i,
                        input=row
                    ),
                    methods=["GET", "POST"]
                )
            return flask.redirect(flask.url_for('processing0'))
        else:
            return "No text in csv file"

    

class SpellCheckerView(MethodView):
    def __init__(self, max_idx, cur_idx, input):
        self.max_idx = max_idx
        self.cur_idx = cur_idx
        self.input = input
    
    def get(self):
        adict = dict()
        result = spell_checker.check(self.input)
        result_dict = result.as_dict()
        for k, v in result_dict.items():
            print(k, v)
        adict['cur_idx'] = self.cur_idx + 1
        adict['max_idx'] = self.max_idx
        adict['original'] = result_dict['original']
        adict['checked'] = result_dict['checked']
        return flask.render_template("spellcheck.html", adict=adict, return_url='/processing{}/'.format(self.cur_idx))
    
    def post(self):
        if self.cur_idx + 1 >= self.max_idx:
            return "finish"
        else:
            return flask.redirect(flask.url_for('processing{}'.format(self.cur_idx + 1)))


class TestPageView(MethodView):
    def __init__(self, test_name="test"):
        self.test_name = test_name

    def get(self):
        ## codes
        return flask.render_template("test.html", adict=adict, audio_root=audio_root, return_url='/{}/'.format(self.test_name))
    
    def post(self):
        flask.request.form.to_dict()
        return flask.redirect(flask.url_for('index'))


app.add_url_rule(
    "/",
    view_func=MainView.as_view("index"),
    methods=["GET", "POST"]
)



app.add_url_rule(
    "/test1/",
    view_func=TestPageView.as_view("test3", test_name="test1"),
    methods=["GET", "POST"]
)

if __name__ == "__main__":
    app.run(
        port=7777,
        # debug=True
    )


