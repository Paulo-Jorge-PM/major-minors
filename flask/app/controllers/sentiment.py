#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Blueprint, render_template
from app.models import db, queries

sentimentRoute = Blueprint('sentiment', __name__,  template_folder='views')

@sentimentRoute.route('/sentiment')
@sentimentRoute.route('/sentiment/<string:minority>')
def sentiment(minority="refugiados"):
    return render_template("sentiment.html", title="Sentiment Analysis | " + minority.capitalize() )
