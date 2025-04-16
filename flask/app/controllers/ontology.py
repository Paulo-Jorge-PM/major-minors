#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from flask import Blueprint, render_template
from app.models import db, queries

views_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'views'))
ontologyRoute = Blueprint('ontology', __name__,  template_folder=views_dir)

@ontologyRoute.route('/ontology')
def ontology():
    return render_template("ontology.html", title="Ontologia")
