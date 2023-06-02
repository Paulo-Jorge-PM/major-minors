#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Blueprint, render_template
from models import db, queries

supportRoute = Blueprint('support', __name__,  template_folder='views')

@supportRoute.route('/support')
def support():
    return render_template("support.html", title="Apoios")
