#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from flask import Blueprint, render_template
from app.models import db, queries

views_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'views'))
scienceRoute = Blueprint('science', __name__,  template_folder=views_dir)

@scienceRoute.route('/science')
def science():
    return render_template("science.html", title="Scientific Output")
