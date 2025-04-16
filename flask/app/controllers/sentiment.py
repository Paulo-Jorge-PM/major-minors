#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from flask import Blueprint, render_template
from app.models import db, queries

views_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'views'))
sentimentRoute = Blueprint('sentiment', __name__,  template_folder=views_dir)

@sentimentRoute.route('/sentiment')
@sentimentRoute.route('/sentiment/<string:minority>')
def sentiment(minority="refugiados"):
    return render_template("sentiment.html", title="Sentiment Analysis | " + minority.capitalize() )
