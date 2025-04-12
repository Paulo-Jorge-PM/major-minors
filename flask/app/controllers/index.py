#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re, json

from flask import Blueprint, render_template, current_app
from app.models import db, queries

indexRoute = Blueprint('index', __name__,  template_folder='views')

### ENDPOINTS
@indexRoute.route('/')
def index():
    data = "teste"

    #totalArticles = db.query(queries.countArticles(), output="csv").replace("countArticles\r\n", "")

    articlesByYear = json.loads(db.query( queries.articlesByYear() ))["results"]["bindings"]
    commentsByYear = json.loads(db.query( queries.commentsByYear() ))["results"]["bindings"]
    imagesByYear = json.loads(db.query( queries.imagesByYear() ))["results"]["bindings"]

    countPartidos = json.loads(db.query( queries.countPartidos() ))["results"]["bindings"][:5]
    countEntities = json.loads(db.query( queries.countEntities() ))["results"]["bindings"][1:6]
    countAnimals = json.loads(db.query( queries.countAnimals() ))["results"]["bindings"][:5]

    totalArticles = 0
    totalComments = 0
    totalImages = 0

    for row in commentsByYear:
        totalComments += int(row['comments']['value'])

    for row in imagesByYear:
        totalImages += int(row['images']['value'])

    for row in articlesByYear:
        totalArticles += int(row['articles']['value'])

    ### NOTA: bug com o output em CSV: XML e JSON retornam o valor correto em double/float p.e. "0.0635789"
    # no entanto em CSV o mesmo valor vem "6.35789", ou seja, retira os zeros iniciais e passa a vírgula na posição a seguir ao 6 :o
    # Deve ser um bug com o graphDB / SPARQL. Era mais fácil tratar em CSV, mas passamos a usar CSV só para valores inteiros por causa disto

    ### Desliguei queries e meti muitos manual para ficar mais rápido
    
    #averageSentiment = db.query(queries.sentimentAverage(), output="xml")
    #averageSentiment = re.sub(r".*#double'>", "", averageSentiment, flags=re.S)
    #averageSentiment = re.sub(r"</literal>.*", "", averageSentiment, flags=re.S)
    #averageSentiment = round(scaleToPercentage(float(averageSentiment)), 2)

    #totalPersons = db.query(queries.totalPersons(), output="csv").replace("persons\r\n", "")
    totalPersons = 23034

    #totalCities = db.query(queries.totalCities(), output="csv").replace("cities\r\n", "")
    totalCities=20540

    #totalCountries = db.query(queries.totalCountries(), output="csv").replace("countries\r\n", "")
    totalCountries=18066

    totalKeywords = db.query(queries.totalKeywords(), output="csv").replace("keywords\r\n", "")
    totalKeywords=26017

    #totaltriples = db.query(queries.totalTriples(), output="csv").replace("triples\r\n", "")
    totaltriples = 5178169

    return render_template("index.html", 
        data=data, 
        title="Homepage",
        totalArticles=totalArticles, 
        #averageSentiment=averageSentiment, 
        totalPersons=totalPersons,
        articlesByYear=articlesByYear,
        imagesByYear=imagesByYear,
        commentsByYear=commentsByYear,
        totalComments=totalComments,
        totalImages=totalImages,
        totalCities=totalCities,
        totalCountries=totalCountries,
        totalKeywords=totalKeywords,
        countPartidos=countPartidos,
        countEntities=countEntities,
        countAnimals=countAnimals,
        totaltriples=totaltriples)


def scaleToPercentage(value, minN=-1, maxN=1):
    return ( ((value - minN) * 100) / (maxN - minN) )
