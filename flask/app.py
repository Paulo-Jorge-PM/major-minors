#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, importlib

from flask import Flask
from flask_cors import CORS
"""from controllers.index import indexRoute
from controllers.api import apiRoute
from controllers.articles import articlesRoute
from controllers.contact import contactRoute
from controllers.data import dataRoute
from controllers.film import filmRoute
from controllers.minorities import minoritiesRoute
from controllers.ontology import ontologyRoute
from controllers.presentation import presentationRoute
from controllers.search import searchRoute
from controllers.sentiment import sentimentRoute
from controllers.sentiment import sentimentRoute
from controllers.sparql import sparqlRoute
from controllers.support import supportRoute
from controllers.webvowl import webvowlRoute"""

from controllers import *

app = Flask(__name__, template_folder='views')
CORS(app)
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']

#Load de todos os controllers na pasta controllers automaticamente em vez de manual um a um
controllers = os.path.join(os.getcwd(), "controllers")
for filename in os.listdir(controllers):
    if filename.endswith(".py") and filename != "__init__.py":
        fName = filename.replace(".py","")
        package = importlib.import_module("controllers."+fName)
        module = getattr(package, fName+"Route")
        app.register_blueprint(module)

"""app.register_blueprint(indexRoute)
app.register_blueprint(apiRoute)
app.register_blueprint(articlesRoute)
app.register_blueprint(contactRoute)
app.register_blueprint(dataRoute)
app.register_blueprint(filmRoute)
app.register_blueprint(minoritiesRoute)
app.register_blueprint(ontologyRoute)
app.register_blueprint(presentationRoute)
app.register_blueprint(searchRoute)
app.register_blueprint(sentimentRoute)
app.register_blueprint(sparqlRoute)
app.register_blueprint(supportRoute)
app.register_blueprint(webvowlRoute)"""

## Global variables for all pages
#@app.context_processor
#def global_data():
    #lang = request.args.get("lang", default="pt", type=None)
    #if lang not in ["pt", "en"]:
    #    lang = "pt"
    #return dict(lang=lang)

## Global headers
#@app.after_request
#def add_header(response):
    #response.headers['Cache-Control'] = 'no-store'
    #return response
