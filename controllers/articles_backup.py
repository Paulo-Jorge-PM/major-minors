#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
from flask import Blueprint, render_template, request
from models import db, queries

from libraries.flask_paginate import Pagination, get_page_parameter

articles_backupRoute = Blueprint('articles_backup', __name__,  template_folder='views')

@articles_backupRoute.route('/articles_backup')
@articles_backupRoute.route('/articles_backup/<string:minority>')
def articles_backup(minority=None):
    idArticle = request.args.get('id', None)

    if idArticle:
        query = queries.getArticles(idArticle)
        results = db.query(query)
        data = json.loads(results)
        data = data["results"]["bindings"][0]
        title = "Artigo"
        return render_template("article.html", title=title, data=data)

    else:
        if minority not in queries.minorities:
            minority = None
        perPage = 10
        total = int(db.query(queries.countArticles(minority=minority), output="csv").replace("countArticles", ""))

        page = request.args.get(get_page_parameter(), type=int, default=1)
        pagination = Pagination(page=page, total=total, bs_version=4, alignment='right', inner_window=3, outer_window=3, per_page=perPage, record_name='artigos')

        query = queries.getArticles(minority=minority, offset=(page-1)*perPage, limit=perPage)
        results = db.query(query)
        data = json.loads(results)

        data = data["results"]["bindings"]

        #hasPreview = hasPreview()

        #check if not empty or will give error in jinja for loop
        #try:
        #    data[0]["title"]
        #except:
        #    data = []

        if minority:
            title = "Artigos - " + minority.capitalize()
        else:
            title = "Artigos - Todos"

        return render_template("articles.html", 
            title=title, 
            data=data, 
            pagination=pagination, 
            minorias=queries.minorities, 
            minority=minority, 
            hasPreview=hasPreview)

def hasPreview(row):
    try:
        if row["preview"]["value"]:
            return True
        else:
            return False
    except:
        return False