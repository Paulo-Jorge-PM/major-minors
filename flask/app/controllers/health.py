#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from flask import Blueprint, Response

views_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'views'))
healthRoute = Blueprint('health', __name__, template_folder=views_dir)


@healthRoute.route('/healthz', methods=['GET'])
def healthz():
    # Liveness probe endpoint: keep it lightweight and non-sensitive.
    return Response("ok\n", status=200, mimetype="text/plain")
