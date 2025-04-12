#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Blueprint, render_template
from app.models import db, queries

contactRoute = Blueprint('contact', __name__,  template_folder='views')

@contactRoute.route('/contact')
def contact():
    return render_template("contact.html", title="Contactos")
