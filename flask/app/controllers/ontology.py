#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Blueprint, render_template
from app.models import db, queries

ontologyRoute = Blueprint('ontology', __name__,  template_folder='views')

@ontologyRoute.route('/ontology')
def ontology():
    return render_template("ontology.html", title="Ontologia")
