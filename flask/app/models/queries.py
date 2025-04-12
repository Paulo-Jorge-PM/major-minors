#!/usr/bin/env python
# -*- coding: UTF-8 -*-

minorities = ["refugiados","mulheres","homossexuais","ciganos","africanos","asiáticos","animais","migrantes"]

def getArticles(articleFileName=None, minority=None, offset=None, limit=None, db="minorias"):
    query = '''select ?id ?dataPub ?title ?subTitle ?preview ?text ?link ?sentiment
    (group_concat(DISTINCT ?animal;separator="|") as ?animal) 
    (group_concat(DISTINCT ?religion;separator="|") as ?religion)
    (group_concat(DISTINCT ?city;separator="|") as ?city)
    (group_concat(DISTINCT ?country;separator="|") as ?country)
    (group_concat(DISTINCT ?continent;separator="|") as ?continent)
    (group_concat(DISTINCT ?otherPlace;separator="|") as ?otherPlace)
    (group_concat(DISTINCT ?politicalParty;separator="|") as ?politicalParty)
    (group_concat(DISTINCT ?entity;separator="|") as ?entity)
    (group_concat(DISTINCT ?person;separator="|") as ?person)
    (group_concat(DISTINCT ?ethnicity;separator="|") as ?ethnicity)
    (group_concat(DISTINCT ?month;separator="|") as ?month)
    (group_concat(DISTINCT ?weekday;separator="|") as ?weekday)
    (group_concat(DISTINCT ?tvChannel;separator="|") as ?tvChannel)
    (group_concat(DISTINCT ?sport;separator="|") as ?sport)
    (group_concat(DISTINCT ?carBrand;separator="|") as ?carBrand)
    (group_concat(DISTINCT ?brand;separator="|") as ?brand)
    (group_concat(DISTINCT ?footballClub;separator="|") as ?footballClub)
    (group_concat(DISTINCT ?keyword;separator="|") as ?keyword)
    '''
    if db=='minorias':
        query += '''
    (group_concat(DISTINCT ?minority;separator="|") as ?minority)
    (GROUP_CONCAT(DISTINCT CONCAT(?minority, "#", STR(?priority));SEPARATOR="|") AS ?minorityPriority)
        '''
    
    query += '''
    where {
    ?article rdf:type :Article .
    '''
    
    if db=='minorias':
        query += '''
    bind(strafter(str(?article), 'minors#') as ?id) .
        '''
    else:
        query += '''
    bind(strafter(str(?article), 'publico#') as ?id) .
        '''
    
    query += '''
    ?article :title ?title .
    ?article :dataPub ?dataPub .
    OPTIONAL { ?article :subTitle ?subTitle . }
    OPTIONAL { ?article :preview ?preview } .
    ?article :link ?link .
    ?article :text ?text .
    ?article :sentimentAnalysis ?sentiment .
    
    '''
    
    if db=='minorias':
        query += '''
    ?article :hasPriority ?m .
    ?m :priority ?priority .
    ?m :referesMinority ?minor .
    ?minor :minority ?minority .
    
        '''
    
    query += '''
    OPTIONAL {  ?article :referesAnimal ?a .
                ?a :animal ?animal . }
    
    OPTIONAL {  ?article :referesReligion ?a .
                ?a :religion ?religion . }

    OPTIONAL {  ?article :referesPoliticalParty ?a .
                ?a :politicalParty ?politicalParty . }

    OPTIONAL {  ?article :referesEntity ?a .
                ?a :entity ?entity . }

    OPTIONAL {  ?article :referesPerson ?a .
                ?a :person ?person . }

    OPTIONAL {  ?article :referesEthnicity ?a .
                ?a :ethnicity ?ethnicity . } 

    OPTIONAL {  ?article :referesKeyword ?a .
                ?a :keyword ?keyword . } 

    OPTIONAL {  ?article :referesMonth ?a . 
                ?a :month ?month . }

    OPTIONAL {  ?article :referesWeekday ?a . 
                ?a :weekday ?weekday . }

    OPTIONAL {  ?article :referesCity ?a . 
                ?a :city ?city . }
    
    OPTIONAL {  ?article :referesCountry ?a . 
                ?a :country ?country . }
    
    OPTIONAL {  ?article :referesContinent ?a . 
                ?a :continent ?continent . }
    
    OPTIONAL {  ?article :referesOtherPlace ?a . 
                ?a :otherPlace ?otherPlace . }

    OPTIONAL {  ?article :referesTvChannel ?a . 
                ?a :tvChannel ?tvChannel . }

    OPTIONAL {  ?article :referesSport ?a . 
                ?a :sport ?sport . }

    OPTIONAL {  ?article :referesCarBrand ?a . 
                ?a :carBrand ?carBrand . }

    OPTIONAL {  ?article :referesBrand ?a . 
                ?a :brand ?brand . }

    OPTIONAL {  ?article :referesFootballClub ?a . 
                ?a :footballClub ?footballClub . }
    '''

    if articleFileName:
        query += '''
        #?article :fileName ?fileName .
        FILTER (CONTAINS(?id , "'''+articleFileName+'''")) .
        '''
    elif minority:
        query += '''
        FILTER (CONTAINS(?minority , "'''+minority+'''")) .
        '''

    query += '''}
    GROUP BY ?id ?dataPub ?title ?subTitle ?preview ?text ?link ?sentiment
    '''
    if db=='minorias':
        query += '''
    ORDER BY DESC(?minorityPriority)
        '''

    if limit:
        query += '''LIMIT ''' + str(limit) + '''
        '''
    if offset:
        query += '''OFFSET ''' + str(offset)

    return query

def countArticles(minority=None):
    query = '''SELECT (COUNT(?title) as ?countArticles) WHERE {
    ?article rdf:type :Article .
    ?article :title ?title .

    '''
    if minority:
        query += '''
        ?article :referesMinority ?m .
        ?m :minority ?minority .
        FILTER (CONTAINS(?minority , "'''+minority+'''")) .
        '''
    query += '''}
    '''
    return query

def countImages(minority=None):
    query = '''SELECT (COUNT(DISTINCT ?imageLink) as ?countImages) WHERE {
    ?article a :Article .
    ?article :hasImage ?img .
    ?img :imageLink ?imageLink.
    Filter ( str(?imageLink)!='') .

    '''
    if minority:
        query += '''
        ?article :referesMinority ?m .
        ?m :minority ?minority .
        FILTER (CONTAINS(?minority , "'''+minority+'''")) .
        '''
    query += '''}
    '''
    return query

def yearsWithArticles(minority=None):
    query = '''SELECT DISTINCT (year(?dataPub) as ?dataPubs) WHERE {
    ?article rdf:type :Article .
    ?article :dataPub ?dataPub .
    '''
    if minority:
        query += '''
        ?article :referesMinority ?m .
        ?m :minority ?minority .
        FILTER (CONTAINS(?minority , "'''+minority+'''")) .
        '''
    query += '''}
    '''
    return query

def countPartidos(minority=None):
    query = '''SELECT ?partido (COUNT(?partido) as ?partidos)
    WHERE {
    ?article a :Article .
    ?article :referesPoliticalParty ?pp.
    ?pp :politicalParty ?partido .
    '''
    if minority:
        query += '''
        ?article :referesMinority ?m .
        ?m :minority ?minority .
        FILTER (CONTAINS(?minority , "'''+minority+'''")) .
        '''
    query += '''}
    GROUP BY ?partido
    ORDER BY DESC(?partidos)
    '''
    return query

def countAnimals(minority=None):
    query = '''SELECT ?animal (COUNT(?animal) as ?animals)
    WHERE {
    ?article a :Article .
    ?article :referesAnimal ?ani.
    ?ani :animal ?animal .
    '''
    if minority:
        query += '''
        ?article :referesMinority ?m .
        ?m :minority ?minority .
        FILTER (CONTAINS(?minority , "'''+minority+'''")) .
        '''
    query += '''}
    GROUP BY ?animal
    ORDER BY DESC(?animals)
    '''
    return query

def countEntities(minority=None):
    query = '''SELECT ?entity (COUNT(?entity) as ?entities)
    WHERE {
    ?article a :Article .
    ?article :referesEntity ?ee.
    ?ee :entity ?entity .
    '''
    if minority:
        query += '''
        ?article :referesMinority ?m .
        ?m :minority ?minority .
        FILTER (CONTAINS(?minority , "'''+minority+'''")) .
        '''
    query += '''}
    GROUP BY ?entity
    ORDER BY DESC(?entities)
    '''
    return query

def articlesByYear(minority=None):
    query = '''SELECT ?year (COUNT(?article) as ?articles)
    WHERE {
    ?article a :Article ; :dataPub ?date .
    BIND (year(?date) AS ?year)
    '''
    if minority:
        query += '''
        ?article :referesMinority ?m .
        ?m :minority ?minority .
        FILTER (CONTAINS(?minority , "'''+minority+'''")) .
        '''
    query += '''}
    GROUP BY ?year
    ORDER BY ?year
    '''
    return query

def commentsByYear(minority=None):
    query = '''SELECT ?year (COUNT(?comment) as ?comments)
    WHERE {
    ?article a :Article ; :dataPub ?date .
    ?article :hasComment ?comment .
    ?article :dataPub ?date .
    BIND (year(?date) AS ?year)
    '''
    if minority:
        query += '''
        ?article :referesMinority ?m .
        ?m :minority ?minority .
        FILTER (CONTAINS(?minority , "'''+minority+'''")) .
        '''
    query += '''}
    GROUP BY ?year
    ORDER BY ?year
    '''
    return query

def imagesByYear(minority=None):
    query = '''SELECT ?year (COUNT(?image) as ?images)
    WHERE {
    ?article a :Article ; :dataPub ?date .
    ?article :hasImage ?image .
    ?article :dataPub ?date .
    BIND (year(?date) AS ?year)
    '''
    if minority:
        query += '''
        ?article :referesMinority ?m .
        ?m :minority ?minority .
        FILTER (CONTAINS(?minority , "'''+minority+'''")) .
        '''
    query += '''}
    GROUP BY ?year
    ORDER BY ?year
    '''
    return query

def countByCities(minority, limit=3):
    query = '''SELECT ?city (COUNT(DISTINCT ?article) as ?articles)
    WHERE
    {
    ?article a :Article . 

    ?article :referesMinority ?m .
    ?m :minority ?minority .
        
    ?article :referesCity ?c .
    ?c :city ?city .

    FILTER (CONTAINS(?minority , "'''+minority+'''")) .

    }
    GROUP BY ?city
    ORDER BY DESC(?articles)
    LIMIT '''+str(limit)+'''
    '''
    return query

def countByCountry(minority, limit=3):
    query = '''SELECT ?country (COUNT(DISTINCT ?article) as ?articles)
    WHERE
    {
    ?article a :Article . 

    ?article :referesMinority ?m .
    ?m :minority ?minority .
        
    ?article :referesCountry ?c .
    ?c :country ?country .

    FILTER (CONTAINS(?minority , "'''+minority+'''")) .

    }
    GROUP BY ?country
    ORDER BY DESC(?articles)
    LIMIT '''+str(limit)+'''
    '''
    return query

def countByKeywords(minority, limit=5):
    query = '''SELECT ?keyword (COUNT(DISTINCT ?article) as ?articles)
    WHERE
    {
    ?article a :Article . 

    ?article :referesMinority ?m .
    ?m :minority ?minority .
        
    ?article :referesKeyword ?k .
    ?k :keyword ?keyword .

    FILTER (CONTAINS(?minority , "'''+minority+'''")) .

    }
    GROUP BY ?keyword
    ORDER BY DESC(?articles)
    LIMIT '''+str(limit)+'''
    '''
    return query



def countByPeople(minority, limit=4):
    query = '''SELECT ?person (COUNT(DISTINCT ?article) as ?articles) ?job
    WHERE
    {
    ?article a :Article . 

    ?article :referesMinority ?m .
    ?m :minority ?minority .
        
    ?article :referesPerson ?p .
    ?p :personName ?person .
    OPTIONAL {?p :hasJob ?j .
    ?j :job ?job .}

    FILTER (CONTAINS(?minority , "'''+minority+'''")) .

    }
    GROUP BY ?person ?job
    ORDER BY DESC(?articles)
    LIMIT '''+str(limit)+'''
    '''
    return query

def countByPoliticalParty(minority, limit=4):
    query = '''SELECT ?party (COUNT(DISTINCT ?article) as ?articles)
    WHERE
    {
    ?article a :Article . 

    ?article :referesMinority ?m .
    ?m :minority ?minority .
        
    ?article :referesPoliticalParty ?p .
    ?p :politicalParty ?party .

    FILTER (CONTAINS(?minority , "'''+minority+'''")) .

    }
    GROUP BY ?party
    ORDER BY DESC(?articles)
    LIMIT '''+str(limit)+'''
    '''
    return query

def countByMinorities():
    query = '''SELECT ?minority (COUNT(DISTINCT ?article) as ?articles)
    WHERE
    {
    ?article a :Article . 

    ?article :referesMinority ?m .
    ?m :minority ?minority .
    '''
    return query

def topArticles(minority=None, limit=6):
    query = '''SELECT ?article ?id ?priority ?title ?preview ?text ?dataPub
    WHERE
    {
    ?article a :Article . 
    bind(strafter(str(?article), 'minors#') as ?id) .
    ?article :title ?title .
    ?article :preview ?preview .
    ?article :text ?text .
    ?article :dataPub ?dataPub .
    ?article :hasPriority ?m .
    ?m :priority ?priority .
    ?m :referesMinority ?mm .
    ?mm :minority ?minority .
    FILTER (CONTAINS(?minority , "'''+minority+'''")) .
    }
    ORDER BY DESC(?priority)
    LIMIT '''+str(limit)+'''
    '''
    return query

def getImages(imageFileName=None, minority=None, offset=None, limit=None):
    query = '''SELECT DISTINCT ?imageLink ?title ?dataPub ?idArticle
    (GROUP_CONCAT(DISTINCT ?minority;separator="|") as ?minority)
    (GROUP_CONCAT(DISTINCT CONCAT(?minority, "#", STR(?priority));SEPARATOR="|") AS ?minorityPriority)
    WHERE
    {
        ?article a :Article .
        bind(strafter(str(?article), 'minors#') as ?idArticle) .
        ?article :title ?title . 
        ?article :dataPub ?dataPub .

        ?article :hasImage ?img .
        ?img :imageLink ?imageLink .
        #BIND(REPLACE(STR(?imageLink),"http.*http","http") AS ?urlJornal).

        ?article :hasPriority ?m .
        ?m :priority ?priority .
        ?m :referesMinority ?minor .
        ?minor :minority ?minority .

        Filter ( str(?imageLink)!='') .

    '''

    if imageFileName:
        query += '''
        FILTER (CONTAINS(?img , "'''+imageFileName+'''")) .
        '''
    elif minority:
        query += '''
        FILTER (CONTAINS(?minority , "'''+minority+'''")) .
        '''

    query += '''}
    GROUP BY ?imageLink ?title ?dataPub ?idArticle
    ORDER BY DESC(?priority) ?dataPub
    '''
    if limit:
        query += '''LIMIT ''' + str(limit) + '''
        '''
    if offset:
        query += '''OFFSET ''' + str(offset)

    return query

def getComment(articleFileName=None, minority=None, offset=None, limit=None):
    query = '''SELECT DISTINCT ?comment ?idArticle ?title ?dataPub
    (GROUP_CONCAT(DISTINCT ?minority;separator="|") as ?minority)
    (GROUP_CONCAT(DISTINCT CONCAT(?minority, "#", STR(?priority));SEPARATOR="|") AS ?minorityPriority)
    WHERE
    {
        ?article a :Article .
        bind(strafter(str(?article), 'minors#') as ?idArticle) .
        ?article :title ?title . 
        ?article :hasComment ?cmt .
        ?cmt :comment ?comment .
        ?article :dataPub ?dataPub .

        ?article :hasPriority ?m .
        ?m :priority ?priority .
        ?m :referesMinority ?minor .
        ?minor :minority ?minority .

    '''

    if articleFileName:
        query += '''
        FILTER (CONTAINS(?fileName , "'''+articleFileName+'''")) .
        '''
    elif minority:
        query += '''
        FILTER (CONTAINS(?minority , "'''+minority+'''")) .
        '''

    query += '''}
    GROUP BY ?comment ?idArticle ?title ?dataPub
    ORDER BY DESC(?priority) ?dataPub
    '''

    if limit:
        query += '''LIMIT ''' + str(limit) + '''
        '''
    if offset:
        query += '''OFFSET ''' + str(offset)

    return query

def sentimentAverage():
    query = '''
    SELECT (AVG(xsd:double(?sentiment)) AS ?average)
    WHERE
    {
        ?article a :Article . 
        ?article :sentimentAnalysis ?sentiment .

    }
    '''
    return query

def totalPersons():
    query = '''SELECT (COUNT(?person) AS ?persons)
    WHERE
    {
        ?article a :Article . 
        ?article :referesPerson ?person .
    }
    '''
    return query

def totalCities():
    query = '''SELECT (COUNT(?city) AS ?cities)
    WHERE
    {
        ?article a :Article . 
        ?article :referesCity ?city .
    }
    '''
    return query

def totalCountries():
    query = '''SELECT (COUNT(?country) AS ?countries)
    WHERE
    {
        ?article a :Article . 
        ?article :referesCountry ?country .
    }
    '''
    return query

def totalKeywords():
    query = '''SELECT (COUNT(?keyword) AS ?keywords)
    WHERE
    {
        ?article a :Article . 
        ?article :referesKeyword ?keyword .
    }
    '''
    return query

def totalPartidos():
    query = '''SELECT (COUNT(?partido) AS ?partidos)
    WHERE
    {
        ?article a :Article . 
        ?article :referesPoliticalParty ?partido .
    }
    '''
    return query

def totalTriples():
    query = '''SELECT (COUNT(*) as ?triples) 
    WHERE { ?s ?p ?o } 
    '''
    return query

def getSentiment():
    query = '''
    SELECT (AVG(xsd:double(?sentiment)) AS ?average)
    WHERE
    {
        ?article a :Article . 
        ?article :sentimentAnalysis ?sentiment .

        {
            SELECT ?positive
            WHERE {
                FILTER(xsd:double(?sentiment) > 0, ?positive)
            }
        }
        SELECT ?negative
            WHERE {
                FILTER(xsd:double(?sentiment) < 0, ?positive)
            }

        bind( (xsd:double(?sentiment) > 0) as ?positive) .

    }
    '''
    return query

def countPositive(minority=None):
    query = '''SELECT (COUNT(?sentiment) as ?count)
    WHERE
    {
    ?article a :Article . 
    ?article :sentimentAnalysis ?sentiment .
    ?article :referesMinority ?m .
    ?m :minority ?minority .
        '''
    if minority:
        query += '''
        FILTER (CONTAINS(?minority , "'''+minority+'''")) .
        '''
    query += '''FILTER(xsd:double(?sentiment) > 0.1).
    #FILTER(xsd:double(?sentiment) > 0).
    }
    '''
    return query

def countNegative(minority=None):
    query = '''SELECT (COUNT(?sentiment) as ?count)
    WHERE
    {
    ?article a :Article . 
    ?article :sentimentAnalysis ?sentiment .
    ?article :referesMinority ?m .
    ?m :minority ?minority .
        '''
    if minority:
        query += '''
        FILTER (CONTAINS(?minority , "'''+minority+'''")) .
        '''
    query += '''FILTER(xsd:double(?sentiment) < 0.1).
    #FILTER(xsd:double(?sentiment) < 0).
    }
    '''
    return query

def countNeutral(minority=None):
    query = '''SELECT (COUNT(?sentiment) as ?count)
    WHERE
    {
    ?article a :Article . 
    ?article :sentimentAnalysis ?sentiment .
    ?article :referesMinority ?m .
    ?m :minority ?minority .
        '''
    if minority:
        query += '''
        FILTER (CONTAINS(?minority , "'''+minority+'''")) .
        '''
    query += '''FILTER(xsd:double(?sentiment) > -0.1 && xsd:double(?sentiment) < 0.1).
    #FILTER(xsd:double(?sentiment) = 0).
    }
    '''
    return query
