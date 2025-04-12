#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Blueprint, request, Response, session
from app.models import db, queries

apiRoute = Blueprint('api', __name__,  template_folder='views')

@apiRoute.route('/api/sparql', methods=['GET', 'POST'])
def sparql():

    if request.method == "GET" or request.method == "POST":
        try:
            if request.method == "GET":
                if 'query' in session:
                    query = session.get('query', None)
                else:
                    query = request.args.get('query', None)
            elif request.method == "POST":
                query = request.get_json()['query']

            limit = request.args.get('limit', None)

            formato = request.args.get('output', None)

            modelo = request.args.get('corpus', "minorias")

            if formato not in ["csv", "json", "xml"]:
                formato = "json"

            if query:
                results = db.query(query, output=formato, corpus=modelo)
                if limit:
                    l=int(limit)+1
                    results = '\n'.join(results.split('\n')[:l])

                if formato=="csv":
                    mime="text/csv"
                elif formato=="xml":
                    mime="text/xml"
                elif formato=="json":
                    mime="application/json"
                return Response(results, mimetype=mime, headers={"Content-disposition":"attachment; filename=dados."+formato})
            else:
                return Response(status=404)
        except:
            return Response(status=404)


