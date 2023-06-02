#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json, re, os
from flask import Blueprint, render_template, request
from models import db, queries

from libraries.flask_paginate import Pagination, get_page_parameter

from functools import lru_cache

imagesRoute = Blueprint('images', __name__,  template_folder='views')

linksNotWork = ['http://ultimahora.publico.clix.pt:80/imagens.aspx/220048?tp=UH&db=IMAGENS',
'http://ultimahora.publico.clix.pt:80/imagens.aspx/219947?tp=UH&db=IMAGENS',
'http://ultimahora.publico.clix.pt:80/imagens.aspx/220173?tp=UH&db=IMAGENS',
'http://ultimahora.publico.clix.pt:80/imagens.aspx/220181?tp=UH&db=IMAGENS',
'http://ultimahora.publico.clix.pt:80/imagens.aspx/220137?tp=UH&db=IMAGENS',
'http://ultimahora.publico.clix.pt:80/imagens.aspx/220985?tp=UH&db=IMAGENS',
'http://ultimahora.publico.clix.pt:80/imagens.aspx/220987?tp=UH&db=IMAGENS',
'http://ultimahora.publico.clix.pt:80/imagens.aspx/220890?tp=UH&db=IMAGENS',
'http://ultimahora.publico.clix.pt:80/imagens.aspx/220932?tp=UH&db=IMAGENS',
'http://ultimahora.publico.clix.pt:80/imagens.aspx/181678?tp=UH&db=IMAGENS',
'http://ultimahora.publico.clix.pt:80/imagens.aspx/221201?tp=UH&db=IMAGENS',
'http://ultimahora.publico.clix.pt:80/imagens.aspx/222692?tp=UH&db=IMAGENS',
'http://ultimahora.publico.clix.pt:80/imagens.aspx/222701?tp=UH&db=IMAGENS',
'http://ultimahora.publico.clix.pt:80/imagens.aspx/223118?tp=UH&db=IMAGENS',
'http://ultimahora.publico.clix.pt:80/imagens.aspx/223243?tp=UH&db=IMAGENS',
'http://ultimahora.publico.clix.pt:80/imagens.aspx/223238?tp=UH&db=IMAGENS',
'http://ultimahora.publico.clix.pt:80/imagens.aspx/222632?tp=UH&db=IMAGENS',
'http://ultimahora.publico.clix.pt:80/imagens.aspx/222561?tp=UH&db=IMAGENS',
]

@imagesRoute.route('/images')
@imagesRoute.route('/images/<string:minority>')
def images(minority=None):
    if minority not in queries.minorities:
        minority = None
    perPage = 12

    ### Versão com cache - mais rápida
    page = request.args.get(get_page_parameter(), type=int, default=1)
    #query = loadJson()
    #query = query["results"]["bindings"]

    #data = []
    #data = query
    
    #NEW 3.0 CACHE
    data = loadJson(minority)

    #RETIRA OS REPETIDOS
    """imgs = []
    for imgKey in range(len(data)):
        jornalUrl = originalURL(data[imgKey]['imageLink']['value'])
        if jornalUrl not in imgs and jornalUrl not in linksNotWork:
            imgs.append(jornalUrl)

            if minority:

                minorias = data[imgKey]['minority']['value'].split('|')
                if minority in minorias:
                    priority = [s for s in data[imgKey]['minorityPriority']['value'].split('|') if minority in s][0].replace(minority+'#','')
                    data[imgKey]['priority'] = int(priority)
                else:
                    data[imgKey] = None
                
            else:
                priority = data[imgKey]['minorityPriority']['value'].split('|')[0].split('#')[1]
                data[imgKey]['priority'] = int(priority)            
        else:
            data[imgKey] = None
    for i in range(0, data.count(None)):
        data.remove(None)
    data = sortList(data, orderKey='priority')"""

    
    start = (page-1)*perPage
    end = start + perPage
    total = len(data)
    data = data[start:end]
    pagination = Pagination(page=page, total=total, bs_version=4, alignment='right', inner_window=3, outer_window=3, per_page=perPage, record_name='imagens')





    ## Versão antiga com query + código
    #page = request.args.get(get_page_parameter(), type=int, default=1)

    ### NOTA : Com as queries sparql vinham muitos repetidos (difícil filtrar, o arquivo.pt guarda link diferente para imagens iguais a cada snapshoot)
    ### E imagens antigas da era clix só davam com link arquivo.pt full, e as modernas só dão sem ele
    ### Por isso foi mais fácil processar em código e limpar do que em queries lentas
    #query = queries.getImages(minority=minority)
    #results = db.query(query, output="json")
    #data = json.loads(results)

    #data = data["results"]["bindings"]

    #RETIRA OS REPETIDOS
    #imgs = []
    #for imgKey in range(len(data)):
    #    jornalUrl = originalURL(data[imgKey]['imageLink']['value'])
    #    if jornalUrl not in imgs:
    #        imgs.append(jornalUrl)
    #    else:
    #        data[imgKey] = None
    #Had to run again with a mark, since deleting ongoing would change keys and go out of range: needed a diff list but this is easier
    #for i in range(0, data.count(None)):
    #    data.remove(None)

    #start = (page-1)*perPage
    #end = start + perPage
    #dataPaged = data[start:end]

    #total = len(data)
    #pagination = Pagination(page=page, total=total, bs_version=4, alignment='right', inner_window=3, outer_window=3, per_page=perPage, record_name='imagens')

    if minority:
        title = "Imagens - " + minority.capitalize()
    else:
        title = "Imagens - Todas"

    return render_template("images.html", title=title, 
        #data=dataPaged, 
        data=data,
        pagination=pagination, 
        minorias=queries.minorities, 
        minority=minority, 
        hasPreview=hasPreview,
        filterLink=filterLink)

@lru_cache(maxsize=10)
def loadJson(minority=None):
    baseDir = os.path.dirname(__file__)
    saveDir = os.path.join('models/images.json')
    with open(saveDir, "r", encoding='utf-8') as file:
        data = file.read()
    query = json.loads(data)
    data = query["results"]["bindings"]
    
    #FILTER
    imgs = []
    for imgKey in range(len(data)):
        jornalUrl = originalURL(data[imgKey]['imageLink']['value'])
        if jornalUrl not in imgs and jornalUrl not in linksNotWork:
            imgs.append(jornalUrl)
            if minority:
                minorias = data[imgKey]['minority']['value'].split('|')
                if minority in minorias:
                    priority = [s for s in data[imgKey]['minorityPriority']['value'].split('|') if minority in s][0].replace(minority+'#','')
                    data[imgKey]['priority'] = int(priority)
                else:
                    data[imgKey] = None
            else:
                priority = data[imgKey]['minorityPriority']['value'].split('|')[0].split('#')[1]
                data[imgKey]['priority'] = int(priority)            
        else:
            data[imgKey] = None
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

def originalURL(url):
    new = re.sub(r'http.*http','http', url)
    new = re.sub(r'&w=[0-9]+&t=[0-9]+,[0-9]','', new)
    return new

def filterLink(fullUrl):
    originalUrl = originalURL(fullUrl)
    if re.search(r'.*publico\.clix\.pt.*', originalUrl) or re.search(r'.*static\.publico\.pt.*aspx.*', originalUrl):
        url = fullUrl
    else:
        url = originalUrl
    return url

def sortList(lista, orderKey='priority', reverse=True):
    new = sorted(lista, key = lambda i: i[orderKey], reverse=reverse)
    return new