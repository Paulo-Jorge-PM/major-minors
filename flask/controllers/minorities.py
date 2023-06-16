#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json, random
from flask import Blueprint, render_template
from models import db, queries

minoritiesRoute = Blueprint('minorities', __name__,  template_folder='views')

@minoritiesRoute.route('/minorities')
@minoritiesRoute.route('/minorities/<string:minority>')
def minorities(minority=None):
    if minority and minority in queries.minorities:
        minority = minority 
    else:
        minority = queries.minorities[0]
    
    articlesByYear = json.loads(db.query( queries.articlesByYear(minority=minority) ))["results"]["bindings"]
    countByCities = json.loads(db.query( queries.countByCities(minority=minority, limit=6) ))["results"]["bindings"]
    countByCountry = json.loads(db.query( queries.countByCountry(minority=minority, limit=6) ))["results"]["bindings"]
    countByKeywords = json.loads(db.query( queries.countByKeywords(minority=minority, limit=10) ))["results"]["bindings"]
    countByPeopleTemp = json.loads(db.query( queries.countByPeople(minority=minority, limit=20) ))["results"]["bindings"]

    #Filter PErson names we don't want to show up (to vague)
    c=0
    countByPeople = []
    for p in countByPeopleTemp:
        if c<5:
            if p["person"]["value"] not in ["Nas", "Amigos", "Fantasia", "Miguel", "James", "Solo", "Live", "Sun", "1981"]:
                countByPeople.append(p)
                c+=1

    countByPoliticalParty = json.loads(db.query( queries.countByPoliticalParty(minority=minority, limit=5) ))["results"]["bindings"]
    topArticles = json.loads(db.query( queries.topArticles(minority=minority, limit=6) ))["results"]["bindings"]

    countPositive = json.loads(db.query( queries.countPositive(minority=minority) ))["results"]["bindings"][0]["count"]["value"][:4]
    countNegative = json.loads(db.query( queries.countNegative(minority=minority) ))["results"]["bindings"][0]["count"]["value"][:4]
    countNeutral = json.loads(db.query( queries.countNeutral(minority=minority) ))["results"]["bindings"][0]["count"]["value"][:4]


    articleImages = []
    for n in range(6):
        n+=1
        articleImages.append(minority+'-'+str(n)+'.jpg')
    random.shuffle(articleImages)

    return render_template(minority+".html", title=None, 
        articlesByYear=articlesByYear, 
        countByCities=countByCities, 
        countByCountry=countByCountry, 
        countByKeywords=countByKeywords,
        countByPeople=countByPeople,
        countByPoliticalParty=countByPoliticalParty,
        topArticles=topArticles,
        articleImages=articleImages,
        minority=minority,
        countPositive=countPositive,
        countNegative=countNegative,
        countNeutral=countNeutral)