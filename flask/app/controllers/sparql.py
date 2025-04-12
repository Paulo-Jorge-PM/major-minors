#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Blueprint, render_template, request, Response, session, jsonify
from app.models import db, queries
from app.libraries import flask_session

sparqlRoute = Blueprint('sparql', __name__,  template_folder='views')

@sparqlRoute.route('/sparql', methods=['GET', 'POST'])
def sparql():
    results=None
    #formato=None
    queryEncoded=None
    limitResults=10000
    external="false"
    #modelo="minorias"

    #Get corpus from POST or from GET
    modelo = request.form.get('corpus')
    if not modelo:
        modelo = request.args.get('corpus', "minorias")
                
    if 'query' in session:
        activeQuery = session['query']
    else:
        activeQuery = None

    if request.method == "POST":
        try:
            
            output = request.args.get('output', "csv")
            external = request.args.get('external', "false")

            if external != "true":
                #query = request.form["query"]
                query = request.form.get('query')
            else:
                query = request.get_json()['query']

            #formato = request.form["formato"]
            #if formato not in ["csv", "json", "xml"]:
            #    formato = "csv"

            results = db.query(query, output=output, corpus=modelo)

            if external == "false":
                results= '\n'.join(results.split('\n')[:60])

            
            queryEncoded = db.queryEncode(query)

            #if 'queryEncoded' in session:  
            #    session.pop('queryEncoded',None)

            session['queryEncoded'] = queryEncoded
            session['query'] = query
            activeQuery = activeQuery = session['query']

            #print(session['queryEncoded'])

            #if formato=="csv":
            #    mime="text/csv"
            #elif formato=="xml":
            #    mime="text/xml"
            #elif formato=="json":
            #    mime="application/json"
            #return Response(results, mimetype=mime, headers={"Content-disposition":"attachment; filename=dados."+formato})
        except:
            pass
    if external == "true":
        return jsonify(results)
    else:
        return render_template("sparql.html", title="Consultas SPARQL" , results=results, queryEncoded=queryEncoded, activeQuery=activeQuery, corpus=modelo)

#@sparqlRoute.route('/download')
#def download():
#    return Response(results, mimetype=mime, headers={"Content-disposition":"attachment; filename=dados."+formato})