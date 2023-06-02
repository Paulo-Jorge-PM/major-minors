#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Blueprint, render_template
from models import db, queries

webvowlRoute = Blueprint('webvowl', __name__,  template_folder='views')

@webvowlRoute.route('/webvowl')
def webvowl():
    return render_template("webvowl.html")
