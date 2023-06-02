#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Blueprint, render_template
from models import db, queries

searchRoute = Blueprint('search', __name__,  template_folder='views')

@searchRoute.route('/search')
def search():
    return render_template("search.html", title="Pesquisa Guiada")
