"""
This is the server module to create a `connexion` application. Run it from the
command line with python for testing.

The application is named to be compatible with uwsgi.
"""

import os

import connexion

PORT = int(os.environ.get('PORT', 5000))
#0.0.0.0 so the port is reachable from outside the container
HOST = os.environ.get('HOST', '0.0.0.0')

application = connexion.App(__name__, port=PORT, specification_dir='')
application.add_api('models.yaml')


if __name__ == '__main__':
    application.run(host=HOST, port=PORT, debug=False)
