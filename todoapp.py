#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A small docstring for Flask web app"""

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import re

app = Flask(__name__)
to_do_list = []
status = ""


class Task:

    def __init__(self, task, owner, priority):
        self.task = task
        self.owner = owner
        self.priority = priority


@app.route('/')
def display():
   
    return render_template('display.html', to_do_list=to_do_list,
                           status=status)


@app.route('/submit', methods=['POST'])
def submit():

    global status
    task = request.form['task']
    owner = request.form['email']
    priority = request.form['priority']

    if task == "":
        status = "Error: You must enter a task."
        return redirect("/")
    else:
        status = ""

    pattern = "^[^@]+[@]{1}[a-zA-Z0-9]+([\-]+[a-zA-Z0-9]+)*([\.]{1}[a-zA-Z" \
              "0-9]+([\-]+[a-zA-Z0-9]+)*)+"

    if not re.search(pattern, owner):
        status = "Error: There was a problem adding the task. Try entering" \
                 " a valid e-mail."
        return redirect("/")
    else:
        status = ""

    if priority != "High" and priority != "Medium" and priority != "Low":
        status = "Error: There was a problem adding the task. Please select" \
                 " a priority."
        return redirect("/")
    else:
        status = ""

    t = Task(task, owner, priority)
    to_do_list.append(t)

    return redirect("/")


@app.route('/clear', methods=['POST'])
def clear():

    del to_do_list[:]
    return redirect("/")


@app.route('/delete', methods=['POST'])
def delete():

    delete_index = int(request.form['index'])
    del to_do_list[delete_index]
    return redirect("/")

if __name__ == "__main__":

    app.run()
