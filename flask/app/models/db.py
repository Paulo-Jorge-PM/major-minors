#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Response
import requests
import urllib.parse, json

### DB configurations

### NOTA: os prefixos retirados do Node não dão no Flask :O Why? Coloquei apenas o prefixo base e já deu
prefixes = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX noInferences: <http://www.ontotext.com/explicit>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX c: <http://sparql.ilch.uminho.pt/minors#>
    
    '''

prefixes = '''PREFIX : <http://sparql.ilch.uminho.pt/minors#>
'''

prefixesPublico = '''PREFIX : <http://sparql.ilch.uminho.pt/publico#>
'''

repository = 'http://graphdb:7200/repositories/minors?query='
repoPulico = 'http://graphdb:7200/repositories/publico?query='
#repoQuery = repository + '?query='

## Outro diferente do exemplo Node:
#repoQuery = 'http://localhost:7200/sparql?name=&infer=true&sameAs=true&query='

def query(query, output="json", corpus="minorias"):
    if corpus == "indiferenciado":
        repo = repoPulico
        prefixe = prefixesPublico
    else:
        repo = repository
        prefixe = prefixes

    encoded = urllib.parse.quote(prefixe + query, safe="~()*!.\'")
    fullUrl = repo + encoded
    print(f"Querying URL: {fullUrl}")

    try:
        #data = fetch.json()
        #data = fetch.text
        #data = fetch.content
        if output=="xml":
            header = {"Accept":"application/sparql-results+xml"}
        elif output=="csv":
            header = {"Accept":"text/csv"}
        elif output=="table":
            header = {"Accept":"application/x-binary-rdf-results-table"}
        else:
            header = {"Accept":"application/sparql-results+json"}

        fetch = requests.get(fullUrl, headers=header)
        print(f"fetch: {fetch}")

        #data = fetch.json()
        data = fetch.text
        #data = json.loads(fetch.text)



        #data = data.replace("'", "\"")
        #data = json.loads(fetch.text)
    except:
        data = "Error - Could not connect with db"
    #return Response(json.dumps(data), mimetype='application/json')

    #d = json.load(data)
    #for element in data:
    #    element.pop('head')
    #return json.dumps(data)
    return data

def queryEncode(query, prefixe=False):
    if prefixe:
        encoded = urllib.parse.quote(prefixes + query, safe="~()*!.\'")
    else:
        encoded = urllib.parse.quote(query, safe="~()*!.\'")
    return encoded


if __name__ == '__main__':
    import queries
    q = queries.getArticles()
    results = query(q)

    q = '''select ?article ?m where {
    ?article rdf:type :Article.
    ?article :referesMinority ?m.
}'''
    #results = query(q)

    print(results)
