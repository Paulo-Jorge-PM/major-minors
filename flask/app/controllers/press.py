#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Blueprint, render_template
from app.models import db, queries

pressRoute = Blueprint('press', __name__,  template_folder='views')

@pressRoute.route('/press')
def press():
    return render_template("press.html", title="Imprensa")
