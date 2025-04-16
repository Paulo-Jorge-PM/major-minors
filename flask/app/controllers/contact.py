#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from flask import Blueprint, render_template
from app.models import db, queries

views_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'views'))
contactRoute = Blueprint('contact', __name__,  template_folder=views_dir)

@contactRoute.route('/contact')
def contact():
    return render_template("contact.html", title="Contactos")
