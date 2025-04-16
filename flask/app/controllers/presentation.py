#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from flask import Blueprint, render_template
from app.models import db, queries

views_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'views'))
presentationRoute = Blueprint('presentation', __name__,  template_folder=views_dir)

@presentationRoute.route('/presentation')
def presentation():
    return render_template("presentation.html", title="Apresentação")
