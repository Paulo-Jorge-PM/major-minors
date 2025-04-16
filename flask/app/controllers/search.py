#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from flask import Blueprint, render_template
from app.models import db, queries

views_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'views'))
searchRoute = Blueprint('search', __name__,  template_folder=views_dir)

@searchRoute.route('/search')
def search():
    return render_template("search.html", title="Pesquisa Guiada")
