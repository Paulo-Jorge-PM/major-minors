#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json, os
from flask import Blueprint, render_template, request
from models import db, queries

from libraries.flask_paginate import Pagination, get_page_parameter

from functools import lru_cache

commentsRoute = Blueprint('comments', __name__,  template_folder='views')

@commentsRoute.route('/comments')
@commentsRoute.route('/comments/<string:minority>')
def comments(minority=None):
    if minority not in queries.minorities:
        minority = None
    perPage = 10
    sortKey = 'priority'

    ### Versão Cache

    page = request.args.get(get_page_parameter(), type=int, default=1)
    #query = loadJson()
    #query = query["results"]["bindings"]
    #data = query
    
    #NEW 3.0 CACHE
    data = loadJson(minority)
    
    """comments = []
    for dicKey in range(len(data)):
        comment = data[dicKey]['comment']['value']
        if comment not in comments:
            comments.append(comment)

            if minority:

                minorias = data[dicKey]['minority']['value'].split('|')
                if minority in minorias:
                    priority = [s for s in data[dicKey]['minorityPriority']['value'].split('|') if minority in s][0].replace(minority+'#','')
                    data[dicKey]['priority'] = int(priority)
                else:
                    data[dicKey] = None
                
            else:
                priority = data[dicKey]['minorityPriority']['value'].split('|')[0].split('#')[1]
                data[dicKey]['priority'] = int(priority)
            
        else:
            data[dicKey] = None
    for i in range(0, data.count(None)):
        data.remove(None)

    data = sortList(data, orderKey='priority')"""


    """page = request.args.get(get_page_parameter(), type=int, default=1)
    query = loadJson()
    query = query["results"]["bindings"]
    data = []
    if minority:
        for row in query:
            minorias = row['minority']['value'].split('|')
            if minority in minorias:
                priority = [s for s in row['minorityPriority']['value'].split('|') if minority in s][0].replace(minority+'#','')
                row['priority'] = int(priority)
                data.append(row)
        data = sortList(data, orderKey=sortKey)

    else:
        data = query
        for row in data:
            priority = row['minorityPriority']['value'].split('|')[0].split('#')[1]
            row['priority'] = int(priority)
        data = sortList(data, orderKey=sortKey)"""

    start = (page-1)*perPage
    end = start + perPage
    total = len(data)
    data = data[start:end]
    pagination = Pagination(page=page, total=total, bs_version=4, alignment='right', inner_window=3, outer_window=3, per_page=perPage, record_name='comentários')

    ## Versão antiga com query
    #total = int(db.query(queries.countArticles(minority=minority), output="csv").replace("countArticles", ""))
    #page = request.args.get(get_page_parameter(), type=int, default=1)
    #pagination = Pagination(page=page, total=total, bs_version=4, alignment='right', inner_window=3, outer_window=3, per_page=perPage, record_name='artigos')
    #query = queries.getComment(minority=minority, offset=(page-1)*perPage, limit=perPage)
    #results = db.query(query)
    #data = json.loads(results)
    #data = data["results"]["bindings"]


    if minority:
        title = "Comentários - " + minority.capitalize()
    else:
        title = "Comentários - Todos"

    return render_template("comments.html", title=title, data=data, pagination=pagination, minorias=queries.minorities, minority=minority, hasPreview=hasPreview)

@lru_cache(maxsize=10)
def loadJson(minority=None):
    baseDir = os.path.dirname(__file__)
    saveDir = os.path.join('models/comments.json')
    with open(saveDir, "r", encoding='utf-8') as file:
        data = file.read()
    query = json.loads(data)
    data = query["results"]["bindings"]
    
    #FILTER
    comments = []
    for dicKey in range(len(data)):
        comment = data[dicKey]['comment']['value']
        if comment not in comments:
            comments.append(comment)

            if minority:
                minorias = data[dicKey]['minority']['value'].split('|')
                if minority in minorias:
                    priority = [s for s in data[dicKey]['minorityPriority']['value'].split('|') if minority in s][0].replace(minority+'#','')
                    data[dicKey]['priority'] = int(priority)
                    #data.append(data[dicKey])
                else:
                    data[dicKey] = None
                
            else:
                priority = data[dicKey]['minorityPriority']['value'].split('|')[0].split('#')[1]
                data[dicKey]['priority'] = int(priority)
                #data = sortList(data, orderKey='priority')
            
        else:
            data[dicKey] = None
    #Had to run again with a mark, since deleting ongoing would change keys and go out of range: needed a diff list but this is easier
    for i in range(0, data.count(None)):
        data.remove(None)

    data = sortList(data, orderKey='priority')
    
    return data
    
def hasPreview(row):
    try:
        if row["preview"]["value"]:
            return True
        else:
            return False
    except:
        return False

def sortList(lista, orderKey='priority', reverse=True):
    new = sorted(lista, key = lambda i: i[orderKey], reverse=reverse)
    return new