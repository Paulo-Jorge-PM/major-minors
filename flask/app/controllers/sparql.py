#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from flask import Blueprint, render_template, request, session

views_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'views'))
sparqlRoute = Blueprint('sparql', __name__,  template_folder=views_dir)
SPARQL_DISABLED_MESSAGE = "Servico de consultas SPARQL temporariamente desativado devido a recursos limitados."

@sparqlRoute.route('/sparql', methods=['GET', 'POST'])
def sparql():
    results = None
    queryEncoded = None
    modelo = request.form.get('corpus')
    if not modelo:
        modelo = request.args.get('corpus', "minorias")
    activeQuery = session.get('query', None)

    # SPARQL execution is intentionally disabled for now.
    # Keep legacy implementation commented for quick future re-enable.
    return render_template(
        "sparql.html",
        title="Consultas SPARQL",
        results=results,
        queryEncoded=queryEncoded,
        activeQuery=activeQuery,
        corpus=modelo,
        sparql_disabled=True,
        sparql_disabled_message=SPARQL_DISABLED_MESSAGE,
    )

#@sparqlRoute.route('/download')
#def download():
#    return Response(results, mimetype=mime, headers={"Content-disposition":"attachment; filename=dados."+formato})
