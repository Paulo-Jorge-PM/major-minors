#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from flask import Blueprint, render_template
from app.models import db, queries

views_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'views'))
dataRoute = Blueprint('data', __name__,  template_folder=views_dir)

@dataRoute.route('/data/<string:data>')
def data(data="pessoas"):
    return render_template("data.html", title="Dados | " + data.capitalize())
