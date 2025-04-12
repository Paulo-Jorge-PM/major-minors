#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Blueprint, render_template
from app.models import db, queries

dataRoute = Blueprint('data', __name__,  template_folder='views')

@dataRoute.route('/data/<string:data>')
def data(data="pessoas"):
    return render_template("data.html", title="Dados | " + data.capitalize())