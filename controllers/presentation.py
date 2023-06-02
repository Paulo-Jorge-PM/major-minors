#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Blueprint, render_template
from models import db, queries

presentationRoute = Blueprint('presentation', __name__,  template_folder='views')

@presentationRoute.route('/presentation')
def presentation():
    return render_template("presentation.html", title="Apresentação")
