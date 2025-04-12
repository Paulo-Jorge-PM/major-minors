#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Blueprint, render_template
from app.models import db, queries

scienceRoute = Blueprint('science', __name__,  template_folder='views')

@scienceRoute.route('/science')
def science():
    return render_template("science.html", title="Scientific Output")
