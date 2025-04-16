#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json, os, re
from flask import Blueprint, render_template, request
from app.models import db, queries

from app.libraries.flask_paginate import Pagination, get_page_parameter

from functools import lru_cache

views_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'views'))
articlesRoute = Blueprint('articles', __name__,  template_folder=views_dir)

@articlesRoute.route('/articles')
@articlesRoute.route('/articles/<string:minority>')
def articles(minority=None):
    idArticle = request.args.get('id', None)
    dbType = request.args.get('db', 'minorias')
    #print(dbType)
    if idArticle:
        query = queries.getArticles(idArticle, db=dbType)
        results = db.query(query, corpus=dbType)
        data = json.loads(results)
        data = data["results"]["bindings"][0]
        title = "Artigo"
        return render_template("article.html", title=title, data=data, db=dbType)

    else:
        if minority not in queries.minorities:
            minority = None
        perPage = 10


        ### NOVA VERSÃO MANUAL MAIS RÁPIDA
        page = request.args.get(get_page_parameter(), type=int, default=1)
        #query = loadJson()
        #query = query["results"]["bindings"]
        #data = query
        #articles = []
        
        #NEW CHACHING SYSTEM - FUNCTIONS RESULTS ARE SAVED, RETURN ONLY ONCE (NEED RESTART SERVER TO LOAD NEW DATA)
        data = loadJson(minority)

        """for dicKey in range(len(data)):
            article = originalURL(data[dicKey]['title']['value'])
            if article not in articles:
                articles.append(article)

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





        '''if minority:
            for row in query:
                minorias = row['minority']['value'].split('|')
                if minority in minorias:
                    priority = [s for s in row['minorityPriority']['value'].split('|') if minority in s][0].replace(minority+'#','')
                    row['priority'] = int(priority)
                    data.append(row)
            data = sortList(data, orderKey='priority')

        else:
            data = query
            for row in data:
                priority = row['minorityPriority']['value'].split('|')[0].split('#')[1]
                row['priority'] = int(priority)
            data = sortList(data, orderKey='priority')'''


        
        start = (page-1)*perPage
        end = start + perPage
        total = len(data)
        data = data[start:end]
        pagination = Pagination(page=page, total=total, bs_version=4, alignment='right', inner_window=3, outer_window=3, per_page=perPage, record_name='artigos')


        ### VERSÃO ORIGINAL SPARQL
        '''total = int(db.query(queries.countArticles(minority=minority), output="csv").replace("countArticles", ""))
        page = request.args.get(get_page_parameter(), type=int, default=1)
        pagination = Pagination(page=page, total=total, bs_version=4, alignment='right', inner_window=3, outer_window=3, per_page=perPage, record_name='artigos')
        query = queries.getArticles(minority=minority, offset=(page-1)*perPage, limit=perPage)
        results = db.query(query)
        data = json.loads(results)
        data = data["results"]["bindings"]'''

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

#CHACHE - EVEN IF DELETE/CHANGE JSON IT WILL USE THE LOADED LAST
#maxsize = No. of saved variations (the minority arg) - there is only 8 minorities or None = 9
@lru_cache(maxsize=10)
def loadJson(minority=None):
    baseDir = os.path.dirname(__file__)
    saveDir = os.path.join('models/articles.json')
    with open(saveDir, "r", encoding='utf-8') as file:
        data = file.read()
    query = json.loads(data)
    data = query["results"]["bindings"]
    
    #FILTER
    articles = []
    for dicKey in range(len(data)):
        article = originalURL(data[dicKey]['title']['value'])
        if article not in articles:
            articles.append(article)
            
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
    data = sortList(data, orderKey='priority')
    return data


def sortList(lista, orderKey='priority', reverse=True):
    new = sorted(lista, key = lambda i: i[orderKey], reverse=reverse)
    return new

def originalURL(url):
    new = re.sub(r'http.*http','http', url)
    new = re.sub(r'/[0-9]+/[0-9]+/[0-9]+','', new)
    new = re.sub(r'&w=[0-9]+&t=[0-9]+,[0-9]','', new)
    new = re.sub(r'\?frm=ult', '', new)
    return new
