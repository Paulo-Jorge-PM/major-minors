#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from flask import Blueprint, render_template
from app.models import db, queries

views_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'views'))
pressRoute = Blueprint('press', __name__,  template_folder=views_dir)

@pressRoute.route('/press')
def press():
    return render_template("press.html", title="Imprensa")
