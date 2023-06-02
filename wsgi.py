#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app import app

# For debugging; will not run if launched from Nginx
if __name__ == "__main__":
    #threaded=True
    app.run(port=8080, debug=True, host="0.0.0.0")
